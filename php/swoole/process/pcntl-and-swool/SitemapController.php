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
     * sitemap的index，默认从0开始
     * @var int
     */
    public $lastIndex = 0;
    public $lastId = 0;
    const URL_PER_FILE = 50000;
    /**
     * 渲染100条记录输入文件一次
     */
    const BUFFER_ROW = 100;
    const SITEMAP_NAME = '/sitemap_%d.xml';
    const SITEMAP_INDEX = '/sitemap_index.xml';
    public $sitemap_path = '';

    public function __construct(){
        parent::__construct();
        //在config里设置不起作用，估计哪里有bug，暂时不去深究
        $this->_viewsHome = ROOT_DIR.'/sbin/views/';

        $this->cola_db = $this->model('Tag')->db();
        $this->logFilePath = ROOT_DIR.'/sbin/sitemap_pic_id.log';
        $this->sitemap_path = ROOT_DIR.'/sites/wwwroot/sitemaps';
        //检测 $this->sitemap_path是否存在，不存在的话创建
        if(!file_exists($this->sitemap_path)){
            mkdir($this->sitemap_path);
        }

        //打开文件或创建文件，并读取上次生成到的id
        $this->openLog();
        // 读取目录下 格式为 sitemap_\d.xml的文件，取得最大的那个index, 作为此次生成文件的基准;
        //如果想重新生成所有，需要删除目录下的所有sitemap文件
        // TODO 可以用参数控制
        $this->setLastIndex();
    }

    public function __destruct(){
        if(is_resource($this->logHandler)){
            fclose($this->logHandler);
        }
    }

    public function openLog(){
        if(file_exists($this->logFilePath)){
            $file = fopen($this->logFilePath, 'r+');
            $this->lastId = file_get_contents($this->logFilePath);
        }else{
            //log不存在
            $file = fopen($this->logFilePath, 'w+');
            $this->lastId = 0;
        }
        $this->logHandler = $file;
    }

    /**
     * 记录本次生成后的最大id，下次从这个id开始生成
     * @param $id
     * @return bool
     */
    public function logMaxIdForThisTime($id){
        rewind($this->logHandler);
        $byte = fwrite($this->logHandler, $id);
        fflush($this->logHandler);
        return $byte>0;
    }

    public function setLastIndex(){
        $maxIndex = 0;
        foreach(glob($this->sitemap_path.'/*.xml') as $filename) {
            preg_match('/.+\/sitemap_(\d+).xml/', $filename, $matches);
            if(isset($matches[1]) && $matches[1]>$maxIndex ){
                $maxIndex = $matches[1];
            }
        }
        $this->lastIndex = $maxIndex;
    }

    public function runAction(){
        //根据max_id, lastIndex,安排job
        $this->calculateJob();

        //生成一个sitemap的index文件
        $this->generateSitemapIndex();
        exit();

        for($i = 0; $i < $this->worker_num; $i++){
            $process = new swoole_process(array($this, 'generate'));
            // 传递job给子进程
            $process->sitemap_job = $this->jobs[$i];
            $pid = $process->start();
            $this->workers[$pid] = $process;
        }

        for($i = 0; $i < $this->worker_num; $i++)
        {
            //阻塞
            $ret = swoole_process::wait();
            $pid = $ret['pid'];
            unset($this->workers[$pid]);
            echo "Worker Exit, PID=".$pid.PHP_EOL;
        }
    }

    public function generateSitemapIndex(){
        $jobs = $this->jobs;
        $jobs = array_reduce($jobs, function($carry, $item){
            $carry = array_merge($carry, array_keys($item));
            return $carry;
        },[]);
        $view = $this->view();
        $view->sitemaps = $jobs;
        $string = $view->fetch('Sitemap/sitemap_index.php');

        //直接覆盖，TODO 如果要增量，必须判断存在与否
        $file = fopen($this->sitemap_path.self::SITEMAP_INDEX, 'w+');
        fwrite($file, "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n <sitemapindex> \n");
        fwrite($file, $string);
        fwrite($file, "</sitemapindex>");
        fflush($file);
        fclose($file);
    }

    public function generate(swoole_process $worker){
        $job = $worker->sitemap_job;
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

    /**
     * 按id分配任务，并且记录当前最大id
     * @param $totalCount
     * @param $workerNum
     */
    public function calculateJob(){
        $maxId = $this->getLastPicId();
        $this->logMaxIdForThisTime($maxId);

        $lastId = $this->lastId;
        $lastIndex = $this->lastIndex;
        if($lastId === $maxId){
            return array();
        }

        $jobs = array();
        $currentIndex = $lastIndex++;
        $worker_index=0;

        while($lastId < $maxId){
            $currentFile = sprintf($this->sitemap_path.self::SITEMAP_NAME, $currentIndex);
            $jobs[$worker_index][$currentFile]['low'] = $lastId;
            $lastId += self::URL_PER_FILE;
            $lastId = min($lastId, $maxId);// lastId不能超过maxId
            $jobs[$worker_index][$currentFile]['high'] = $lastId;

            $currentIndex++;
            if($worker_index<3){
                $worker_index++;
            }else{
                $worker_index = 0;
            }
        }

        $this->jobs = $jobs;
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
                where p.id>= $lowId and p.id<$highId limit $offset, $limit";
        return $this->cola_db->sql($sql);
    }


    public function getLastPicId(){
        $sql = "select picture_id as id from picture_infos ORDER BY picture_id desc limit 0, 1";
        $result = $this->cola_db->sql($sql);
        return $result[0]['id'];
    }


    public function getTagIdByName($name){
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
    }



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
