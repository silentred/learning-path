<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2015/6/5
 * Time: 9:33
 */

class SitemapController extends Cola_Controller {
    protected $logFilePath;
    protected $logHandler;
    protected $cola_db;
    /**
     * 分配好的job，结构类似$jobs[0][sitemap_file_name] = [区间]
     * @var array
     */
    public $jobs;
    /**
     * 存放子进程，结构为 $workers[$pid] = $process;
     */
    public $workers;
    public $worker_num = 4;
    /**
     * 此次生成sitemap的index，默认从0开始
     * @var int
     */
    public $currentIndex = 0;
    const URL_PER_FILE = 50000;
    /**
     * 渲染100条记录输入文件一次
     */
    const BUFFER_ROW = 100;
    const SITEMAP_NAME = '/sitemap_%d.xml';
    const SITEMAP_INDEX = '/sitemap_index.xml';
    /**
     * sitemaps存放的位置
     * @var string
     */
    public $sitemap_path;
    /**
     * 此次计算任务需要生成的sitemap文件数组，
     * @var array
     */
    public $generatingFiles = array();
    /**
     * 是否是增量
     * @var bool
     */
    public $delta = false;
    public $currentTime;
    public $generate = false;
    public $push = false;

    /**
     * UNIX time, 上次执行的时间
     * @var int
     */
    public $lastTime=0;

    public function __construct(){
        parent::__construct();
        //在config里设置不起作用，估计哪里有bug，暂时不去深究
        $this->_viewsHome = ROOT_DIR.'/sbin/views/';

        $this->cola_db = $this->model('Tag')->db();
        $this->logFilePath = ROOT_DIR.'/sbin/sitemap_last_time.log';
        $this->sitemap_path = ROOT_DIR.'/sites/wwwroot/sitemaps';

        //检测 $this->sitemap_path是否存在，不存在的话创建
        if(!file_exists($this->sitemap_path)){
            mkdir($this->sitemap_path);
        }

        // 参数-d 或者 --delta, -p = push, -g = generate sitemap
        $options = getopt("dpg", array('delta'));
        if(isset($options['d']) || isset($options['delta'])){
            $this->delta = true;
        }
        if(isset($options['g'])){
            $this->generate = true;
        }
        if(isset($options['p'])){
            $this->push = true;
        }

        $this->currentTime = time();

        //打开文件或创建文件，并读取上次生成到的time
        $this->openLog();
        // 读取目录下 格式为 sitemap_%d.xml的文件，取得最大的那个index, 作为此次生成文件的基准;
        //如果想重新生成所有，需要删除目录下的所有sitemap文件
        // 可以用参数控制
        $this->setCurrentIndex();
    }

    public function __destruct(){
        if(is_resource($this->logHandler)){
            fclose($this->logHandler);
        }
    }

    public function openLog(){
        if(file_exists($this->logFilePath)){
            $file = fopen($this->logFilePath, 'r+');
            $this->lastTime = file_get_contents($this->logFilePath);
        }else{
            //log不存在
            $file = fopen($this->logFilePath, 'w+');
            $this->lastTime = 0;
        }
        //如果不是增量，lastTime设为0
        if(!$this->delta || empty($this->lastTime))
            $this->lastTime = 0;

        $this->logHandler = $file;
    }

    /**
     * 记录本次生成的时间，下次生成从这个时间点开始增量
     * @param $id
     * @return bool
     */
    public function logTime($time){
        rewind($this->logHandler);
        $byte = fwrite($this->logHandler, $time);
        fflush($this->logHandler);
        return $byte>0;
    }

    public function setCurrentIndex(){
        $maxIndex = 0;
        $match_time = 0;
        // 如果是增量更新，找到最大的index；否则返回0，从0开始覆盖
        if($this->delta){
            foreach($files = glob($this->sitemap_path.'/*.xml') as $filename) {
                $match_time += preg_match('/.+\/sitemap_(\d+).xml/', $filename, $matches);
                if(isset($matches[1]) && $matches[1]>$maxIndex ){
                    $maxIndex = $matches[1];
                }
            }
            //如果有匹配到文件，说明已经生成过了，此次index需要+1；如果没比配到文件，说明此次从0开始
            if($match_time>0){
                $maxIndex++;
            }
        }
        $this->currentIndex = $maxIndex;
    }

    public function runAction(){
        //根据max_id, currentIndex,安排job
        $this->calculateJob();

        // 参数 -g 判断是否需要生成sitemap
        if($this->generate){
            echo "Starting generating sitemaps...";
            //生成一个sitemap的index文件
            $this->generateSitemapIndex();

            for($i = 0; $i < $this->worker_num; $i++){
                $process = new swoole_process(array($this, 'generate'));
                // 传递job给子进程
                if(isset($this->jobs[$i])){
                    $process->sitemap_job = $this->jobs[$i];
                }
                $pid = $process->start();
                $this->workers[$pid] = $process;
            }

            for($i = 0; $i < $this->worker_num; $i++)
            {
                //阻塞
                $ret = swoole_process::wait();
                $pid = $ret['pid'];
                unset($this->workers[$pid]);
                echo "Generator Worker Exit, PID=".$pid.PHP_EOL;
            }

            echo "Finishing generating sitemaps...";
        }


        // 参数 -p 判断是否需要推送url
        // 一次提交100条，开4个进程，
        if($this->push){
            echo "Starting pushing urls...";
            for($i = 0; $i < $this->worker_num; $i++){
                $process = new swoole_process(array($this, 'push'));
                // 传递job给子进程
                if(isset($this->jobs[$i])){
                    $process->sitemap_job = $this->jobs[$i];
                }
                $pid = $process->start();
                $this->workers[$pid] = $process;
            }

            for($i = 0; $i < $this->worker_num; $i++)
            {
                //阻塞
                $ret = swoole_process::wait();
                $pid = $ret['pid'];
                unset($this->workers[$pid]);
                echo "Push Worker Exit, PID=".$pid.PHP_EOL;
            }
            echo "Finishing pushing urls...";
        }

    }

    public function generateSitemapIndex(){
        $jobs = $this->jobs;
        $jobs = array_reduce($jobs, function($carry, $item){
            $carry = array_merge($carry, array_keys($item));
            return $carry;
        },[]);

        $this->generatingFiles = $jobs;

        $view = $this->view();
        $view->sitemaps = $jobs;
        $string = $view->fetch('Sitemap/sitemap_index.php');

        //非增量，直接覆盖
        if(!$this->delta){
            $file = fopen($this->sitemap_path.self::SITEMAP_INDEX, 'w+');
            fwrite($file, "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n <sitemapindex> \n");
            fwrite($file, $string);
            fwrite($file, "</sitemapindex>");
            fflush($file);
            fclose($file);
        }else{
            // TODO 增量处理
        }

    }

    public function generate(swoole_process $worker){
        $job = null;
        if(isset($worker->sitemap_job)){
            $job = $worker->sitemap_job;
        }
        //先判断这个job是否为空；
        if(empty($job)){
            exit(0);
        }

        //需要新的mysql连接
        $config = (array)Cola::config()->get('_db') + array('adapter' => 'Mysql', 'params' => array());
        $db = Cola_Com_Db::factory($config);
        $this->cola_db = $db;

        //取出keys
        $files = array_keys($job);
        foreach($files as $file){
            //open this file ， w+；不存在就创建，并且truncate文件
            $fileHandler = fopen($file, 'w+');

            $this->writeHeader($fileHandler);

            $low_id = $job[$file]['low'];
            $high_id = $job[$file]['high'];
            // count，从low到high有多少条记录
            $count = $this->countPic($low_id, $high_id);
            $times = $count/self::BUFFER_ROW;
            //如果times为0，也会运行一次$offset=0，可以达到目的
            foreach(range(0, $times) as $index){
                $offset = $index*self::BUFFER_ROW;
                $pics = $this->selectPics($offset, $low_id, $high_id);
                $buffer_string = $this->fetchView($pics);
                fwrite($fileHandler,$buffer_string);
            }

            $this->writeFooter($fileHandler);
            fflush($fileHandler);
            fclose($fileHandler);
        }
    }

    public function push(swoole_process $worker){
        $job = null;
        if(isset($worker->sitemap_job)){
            $job = $worker->sitemap_job;
        }
        //先判断这个job是否为空；
        if(empty($job)){
            exit(0);
        }
        //需要新的mysql连接
        $config = (array)Cola::config()->get('_db') + array('adapter' => 'Mysql', 'params' => array());
        $db = Cola_Com_Db::factory($config);
        $this->cola_db = $db;

        //取出keys
        $files = array_keys($job);
        foreach($files as $file){
            $low_id = $job[$file]['low'];
            $high_id = $job[$file]['high'];
            // count，从low到high有多少条记录
            $count = $this->countPic($low_id, $high_id);
            $times = $count/self::BUFFER_ROW;
            //如果times为0，也会运行一次$offset=0，可以达到目的
            foreach(range(0, $times) as $index){
                $offset = $index*self::BUFFER_ROW;
                $pics = $this->selectPics($offset, $low_id, $high_id);
                $this->pushToBaidu($pics);
            }
        }

    }

    function writeHeader($fd){
        fwrite($fd, "<?xml version=\"1.0\" encoding=\"UTF-8\"?> \n <urlset> \n");
    }

    function writeFooter($fd){
        fwrite($fd, "</urlset> \n");
    }

    function countPic($lowId, $highId){
        $sql = "select count(*) as `count` from pictures where id>= $lowId and id<$highId";
        $ret = $this->cola_db->sql($sql);
        return $ret[0]['count'];
    }

    function fetchView($pics){
        $view = $this->view();
        $view->pics = $pics;
        return $view->fetch('Sitemap/body_segment.php');
    }

    public function pushToBaidu($pics){
        $urls = array_map(function($item){
            return 'http://www.99kk.com/picture/'.$item['id'].'.html';
        }, $pics);

        $api = 'http://data.zz.baidu.com/urls?site=www.99kk.com&token=wZVWOT7UH8nwvMId';
        $ch = curl_init();
        $options =  array(
            CURLOPT_URL => $api,
            CURLOPT_POST => true,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POSTFIELDS => implode("\n", $urls),
            CURLOPT_HTTPHEADER => array('Content-Type: text/plain'),
        );
        curl_setopt_array($ch, $options);
        $result = curl_exec($ch);
        $result = json_decode($result);
        if($result['remain'] <= 0){
            $date = date('Y-m-d H:i:s');
            echo "{$date} - Exceed the url limit today - id is {$urls[0]} \n ";
            exit(0);
        }
        echo "Success: {$result['success']}, left {$result['remain']} to push \n ";
    }

    /**
     * 按lastTime分配任务，并且记录当前time
     * @param $totalCount
     * @param $workerNum
     */
    public function calculateJob(){
        $this->logTime($this->currentTime);

        $count = (int)$this->countNamedPic();
        if($count == 0){
            return array();
        }

        $jobs = array();
        $offset = 0;
        $lastId = 0;
        $worker_index=0;
        $currentIndex = $this->currentIndex;
        while($count>0){
            $currentFile = sprintf($this->sitemap_path.self::SITEMAP_NAME, $currentIndex);
            $jobs[$worker_index][$currentFile]['low'] = $lastId;
            //查找 前500000个 的最大id, limit 1*50000, 1;
            $offset++;
            $count -= self::URL_PER_FILE;
            //如果count很少，不够50000， 则取最大的id
            if($count<0){
                $lastId = $this->getLastId();
            }else{
                $lastId = $this->maxIdByOffset($offset);
            }
            $jobs[$worker_index][$currentFile]['high'] = $lastId;


            $currentIndex++;
            if($worker_index++ >3 ){
                $worker_index = 0;
            }
        }
        $this->jobs = $jobs;
    }

    public function countNamedPic(){
        $sql = "select count(*) as `count` from pictures
          where uptime>{$this->lastTime} and uptime<{$this->currentTime} and name_status=1";
        $ret = $this->cola_db->sql($sql);
        return $ret[0]['count'];
    }

    public function maxIdByOffset($offset){
        $offset *= self::URL_PER_FILE;
        $sql ="select id from pictures
            where uptime>{$this->lastTime} and uptime<{$this->currentTime}
            and name_status=1 limit {$offset},1";
        $ret = $this->cola_db->sql($sql);
        return $ret[0]['id'];
    }

    public function getLastId(){
        $sql ="select id from pictures
            where uptime>{$this->lastTime} and uptime<{$this->currentTime}
            and name_status=1 ORDER BY id DESC limit 0,1";
        $ret = $this->cola_db->sql($sql);
        return $ret[0]['id'];
    }

    public function selectPics($offset, $lowId, $highId, $limit = self::BUFFER_ROW){
        $sql = "select p.id, pi.filesize, pi.filetype, p.`name`,
                DATE_FORMAT(FROM_UNIXTIME(p.`uptime`), '%Y-%m-%d') as `uptime`,
                #c.`name` as cname, cp.`name` as pcname
                CONCAT_WS(' > ',  cp.`name`, c.`name`) as cats
                from pictures as p
                LEFT JOIN picture_infos as pi
                ON p.id = pi.picture_id
                LEFT JOIN categories as c
                ON c.id = p.cate_id
                LEFT JOIN categories as cp
                ON c.pid = cp.id
                where p.id>= $lowId and p.id<$highId and p.name_status=1 limit $offset, $limit";
        return $this->cola_db->sql($sql);
    }


    /*public function getTagIdByName($name){
        $name = addslashes($name);
        $sql = "select * from tags_en where name = '{$name}' ";
        $tag = $this->cola_db->sql($sql);
        if(count($tag)){
            return $tag[0]['id'];
        }else{
            $sql = "insert into tags_en (name) VALUES('{$name}')";
            $lastId = $this->cola_db->sql($sql);
            return $lastId;
        }
    }

    public function insertRelation($tagId, $picId, $confidence){
        $sql = "insert IGNORE into tag_en_pic (tag_en_id, picture_id, confidence) VALUES ({$tagId}, {$picId}, {$confidence})";
        return $this->cola_db->sql($sql);
    }*/



    /*public function logId($id){
        if(is_resource($this->logHandler)){
            rewind($this->logHandler);
            $byte = fwrite($this->logHandler, strval($id));
            fflush($this->logHandler);
            if($byte) return true;
        }
        return false;
    }

    public function getLogId(){
        if(is_resource($this->logHandler)){
            rewind($this->logHandler);
            $result = '';
            while(!feof($this->logHandler)){
                $result .= fread($this->logHandler, 1024);
            }
            return $result;
        }
        return false;
    }*/



}
