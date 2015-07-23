<?php
/**
 * Created by PhpStorm.
 * User: Administrator
 * Date: 2015/6/5
 * Time: 9:33
 */

class TaggingController extends Cola_Controller {
    protected $baseModel;
    protected $logFilePath;
    protected $logHandler;
    protected $api_key = "acc_49865253f7553c4"; // 填写api_key
    protected $api_secret = "b55060fb221dbbd008d67a906be31ade";
    protected $api_base;
    protected $cola_db;
    protected $dbs;

    public function __construct(){
        parent::__construct();
        $this->cola_db = $this->model('Tag')->db();
        $this->logFilePath = ROOT_DIR.'/sbin/pic_id.log';
        $this->logHandler = fopen($this->logFilePath, 'r+');
        $this->api_base = base64_encode($this->api_key.":".$this->api_secret);
    }

    public function __destruct(){
        if(is_resource($this->logHandler)){
            fclose($this->logHandler);
        }
    }

    public function runAction(){
        //get log id
        $pic_id = intval($this->getLogId());

	//die(var_dump($pic_id));
        //取得为标签图片(id, url)
        $workerNum = 5;
        $limit = 20;
        $totalCount = $this->countUntaggedPic($pic_id);
        $partTotalCount = $totalCount/$workerNum;

        $jobs = $this->calculateJob($totalCount, $workerNum, $pic_id);
        var_dump($jobs);
        if($jobs){
            foreach($jobs as $index => $range){
                $pid = pcntl_fork();
                if(!$pid){
                    //子进程
                    $endId = $range['endId'];
                    if(file_exists(ROOT_DIR."/sbin/child_pic_id_{$index}.log")){
                        $pid_log_file = fopen("child_pic_id_{$index}.log", 'r+');
                        $startId = (int)file_get_contents(ROOT_DIR."/sbin/child_pic_id_{$index}.log");
                    }else{
                        //log不存在
                        $pid_log_file = fopen("child_pic_id_{$index}.log", 'w+');
                        $startId = $range['startId'];
                    }

                    //新建一个mysql连接，抛弃原来的
                    $config = (array)Cola::config()->get('_db') + array('adapter' => 'Mysql', 'params' => array());
                    $db = Cola_Com_Db::factory($config);
                    $this->cola_db = $db;
                    //$this->dbs["DB_".$index] = $db;

                    $times = $partTotalCount/$limit +1;

                    for($i=0; $i<$times; $i++){
                        $offset = $i*$limit;
                        $pics = $this->getUntaggedPicWithEnd($startId, $endId, $offset, $limit);

                        foreach($pics as $pic){
                            $id = $pic['id'];
                            $pic_url = $this->getPicUrl($pic['orig_path']);
                            $this->handle($pic_url, $id);
                        }

                        //log pic_id
                        rewind($pid_log_file);
                        fwrite($pid_log_file, $id);
                        fflush($pid_log_file);
                    }

                    //子进程退出时需要关闭资源
                    $this->cola_db->close();
                    fclose($pid_log_file);
                    echo "Child runs to end";
                }
            }

            //父进程等待子进程结束
            while (pcntl_waitpid(0, $status) != -1) {
                $status = pcntl_wexitstatus($status);
                echo "Child $status completed\n";
            }

        }else{
            //没有jobs，不需要多进程
            $times = $totalCount/$limit + 1;
            for($i=0; $i<$times; $i++){
                $offset = $i*$limit;
                $pics = $this->getUntaggedPic($pic_id, $offset, $limit);
                foreach($pics as $pic){
                    $id = $pic['id'];
                    $pic_url = $this->getPicUrl($pic['orig_path']);
                    $this->handle($pic_url, $id);
                }
                $this->logId($id);
            }
        }

    }

    /**
     * 根据未处理的数量 和 进程数量 ，求出每一个
     * @param $totalCount
     * @param $workerNum
     */
    public function calculateJob($totalCount, $workerNum, $lastId){
        $rowPerPart = $totalCount/$workerNum;
        if($rowPerPart == 0){
            return false;
        }
        $result = array();
        $startId = 0;
        $endId = 0;
        foreach(range(1, $workerNum) as $index){
            $offset = (int)($index-1)*$rowPerPart;
            $nextOffset = (int)$index*$rowPerPart;
            if($index == $workerNum && $endId>0){
                //最后一次计算
                $startId = $endId;
                $endId = $this->getLastPicId();
            }elseif($endId > 0){
                //第二次到倒数第二次计算
                $startId = $endId;
                $endId = $this->getStartId($nextOffset, $lastId);
            }else{
                // 第一次计算
                $startId = $this->getStartId($offset, $lastId);
                $endId = $this->getStartId($nextOffset, $lastId);
            }

            $result[$index]['startId'] = $startId;
            $result[$index]['endId'] = $endId;
        }

        return $result;
    }

    public function getStartId($offset, $lastId){
        $offset = intval($offset);
        $sql = "select picture_id as id from picture_infos where picture_id > $lastId and tag_ids=0 limit $offset, 1";
        $result = $this->cola_db->sql($sql);
        return $result[0]['id'];
    }

    public function getLastPicId(){
        $sql = "select picture_id as id from picture_infos where tag_ids=0 ORDER BY picture_id desc limit 0, 1";
        $result = $this->cola_db->sql($sql);
        return $result[0]['id'];
    }

    public function startRequest($startPicId, $pid){

    }

    public function getUntaggedPicWithEnd($startId, $endId, $offset, $limit=20){
        $sql = "select picture_id as id, orig_path from picture_infos where picture_id > $startId and picture_id<= $endId
            and tag_ids=0 limit $offset, $limit";
        return $this->cola_db->sql($sql);
    }



    public function getUntaggedPic($lastId, $offset, $limit=20){
        $sql = "select picture_id as id, orig_path from picture_infos where picture_id > $lastId and tag_ids=0 limit $offset, $limit";
        return $this->cola_db->sql($sql);
    }

    public function countUntaggedPic($lastId){
        $sql = "select count(*) from picture_infos where tag_ids=0 and picture_id > $lastId";
        $count = $this->cola_db->sql($sql);
        if(count($count)){
            return $count[0]['count(*)'];
        }
        return false;
    }

    public function getPicUrl($pic_url){
        return 'http://lt.7kk.com/upload'.$pic_url;
    }

    public function handle($pic_url, $pic_id){
        //重试3次，非常不稳定。
        /**
         * 如果服务器错误会返回
         * array(2) {
                ["status"]=>
                int(500)
                ["message"]=>
                string(21) "Internal Server Error"
            }
         */
        $retries = 3;
        $result = array();
        while($retries>0 && !isset($result['results'])){
            $result = $this->getTags($pic_url, $pic_id);
            $result = json_decode($result,true);

            $retries--;
        }

        if($result){
            // 判断是否有 result, 没有则记录$pic_id，并直接return
            if(!isset($result['results'])){
                echo 'Error #: server error, no results - Pic_id: '.$pic_id ."\n"  ;
                return ;
            }

            $tags = $result['results'][0]['tags']; //(confidence, tag)
			$limit = 30;
			$cnt = 0;
            foreach($tags as $tag){
                // 取前30个tag
				$cnt++;
				if($cnt >= $limit){
					break;
				}
                $tagId = $this->getTagIdByName($tag['tag']);
                $this->insertRelation($tagId, $pic_id, $tag['confidence']);
            }
        }
        //sleep(2);

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

    public function getTags($pic_url, $pic_id){
        $curl = curl_init();

        curl_setopt_array($curl, array(
            CURLOPT_URL => "http://api.imagga.com/v1/tagging?url={$pic_url}&version=2",
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => "",
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => "GET",
            CURLOPT_HTTPHEADER => array(
                "accept: application/json",
                "authorization: Basic {$this->api_base}"
            ),
        ));

        $response = curl_exec($curl);
        $err = curl_error($curl);

        curl_close($curl);

        if ($err) {
	    //die(var_dump($err.$pic_id));
            echo "cURL Error #:" . $err . ' - Pic_id: '.$pic_id ."\n" ;
        } else {
            return $response;
        }
        return false;

    }

    public function logId($id){
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
    }



}
