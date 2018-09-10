<?php
/*
 * watchDog日志存储 Elasticsearch 操作model
 * @author chenshangwei@120.net
 */
class Model_Es {
    private $client = NULL;
    public function __construct()
    {
        //$host = ['219.239.89.198'];
        $host = ['127.0.0.1'];
        require ROOT.'vendor/autoload.php';
        $this->client = Elasticsearch\ClientBuilder::create()->setHosts($host)->build();//->setRetries(0)
    }
    //索引列表
    public function list_index()
    {
        $response = $this->client->indices()->getMapping();
        return array_keys($response);
    }
    //指定索引的type
    public function list_type_by_index($index)
    {
        $response = $this->client->indices()->getMapping(['index' => $index]);
        return isset($response[$index]['mappings'])?array_keys($response[$index]['mappings']):array();
    }
    //写入一个文档索引
    public function add_document($index,$type,$body)
    {
        $params = [
            'index' => $index,
            'type' => $type,
            'body' => $body
        ];
        return $this->client->index($params);
    }
    //一次写入多个文档
    public function add_documents($index,$type,$bodys)
    {
        foreach ($bodys as $val) {
            $params['body'][] = [
                'index' => [
                    '_index' => $index,
                    '_type' => $type,
        	   ]
            ];
            $params['body'][] = $val;
        }
        return $this->client->bulk($params);
    }
    //获取指定的文档
    public function get_document($index,$type,$_id)
    {
        $params = [
            'index' => $index,
            'type' => $type,
            'id' => $_id
        ];
        return $this->client->get($params);
    }
    //删除指定的文档
    public function del_document($index,$type,$_id)
    {
        $params = [
            'index' => $index,
            'type' => $type,
            'id' => $_id
        ];
        try{
            $this->client->delete($params);
            return TRUE;
        }catch(Exception $e){
            return FALSE;
        }
        
    }
    public function test($kw,$index='',$type=''){
    	
    	$params = [
    			"from" => 0,
    			"size" => 10,
    	];
    	if ($index){
    		$params['index'] = $index;
    		if ($type){
    			$params['type'] = $type;
    		}
    	}
    	$params['body']['query']['filtered']['query']['query_string']['query'] = strtolower($kw);
    	$dat = $this->client->search($params);   // Execute the search
    	echo '<pre>';
    	print_r($dat);
    }
    //搜索接口 结果按时间倒序
    public function search($kw='',$index="",$type="",$field='',$time_s=0,$time_e=0,$from=0,$size=10)
    {
    	$re_old = array('，','、','：',':','（','）','*','%','！','@','#','$','^','&','+','-',".",",",'!','|',"/","_");
    	$re_new = array('\，','\、','\：','\:','\（','\）','\*','\%','\！','\@','\#','\$','\^','\&','\+','\-',"\.","\,",'\!','\|',"\/","\_");
    	//$kw= str_replace($re_old,$re_new,$kw);
    	//$kw = urlencode($kw);
    	//echo $kw.'<br />';
    	$keyword = $kw;
        $data = array();
        $params = [
            "from" => $from,
            "size" => $size,
             "body" => [
                'sort' => [
                    //['time' => ['order' => 'desc']],
                	//['_id' => ['order' => 'asc']],
                	['addtime' => ['order' => 'desc']],
                ],
            ] 
        ];
        /* if (!$kw){
        	//if (isset($_GET['test'])){
        		//$params['body']['sort']['_id']['order'] = 'desc';
        	//}else{
        		$params['body']['sort']['time']['order'] = 'desc';
        	//}
        	
        } */
        if ($index){
            $params['index'] = $index;
            if ($type){
                $params['type'] = $type;
            }
        }
        if (!$kw){
            $params['body']['query']['match_all'] = [];
            $params['body']['sort'][]['addtime']['order'] = 'desc';
        }else{
            //$kw = addslashes($kw);
            //$kw = urlencode($kw);
            if ($field){
            	$params['body']['query']['filtered']['query']['match'][$field] = strtolower($kw);
                //$params['body']['highlight']['fields'][$field] = new \stdClass();
            }else{
            	
            	$params['body']['query']['filtered']['query']['query_string']['query'] = strtolower(str_replace($re_old,$re_new,$kw));
                //if (isset($_GET['ooxx'])){
                	/* $kw = str_replace(':','\\:',$kw);
                	$kw = str_replace("-",'\-',$kw); */
                	//$params['body']['query']['match_phrase']['msg'] = $kw;
                	//$params['body']['query']['fuzzy']['msg']= strtolower($kw);
                	//$params['body']['query']['match']['msg']= $kw;
                	//$params['body']['query']['filtered']['query']['query_string']['query'] = strtolower($kw);
                	//unset($params['body']['sort']);
                	//var_dump($params);
                	//$params['body']['sort']['addtime']['order'] = 'desc';
                //}else{
                	//$params['body']['query']['filtered']['query']['query_string']['query'] = $kw;
                	//$params['body']['query']['fuzzy']['msg']= strtolower($kw);
                	//$params['body']['query']['filtered']['query']['query_string']['query'] = strtolower($kw);
                //}
            }
        }
        //if ($index == '120ask' && $type == 's' ){ //特别处理 && isset($_GET['ooxx'])
        	//unset($params['body']['sort']);
       // $params['body']['sort'][]['addtime']['order'] = 'desc';
        //}
        if ($time_s > 0){
            $params['body']['filter']['range']['time']['gte'] = $time_s;
        }
        if ($time_e > 0){
           $params['body']['filter']['range']['time']['lte'] = $time_e;
        }
        //$params['body']['highlight']['fields']['msg'] = new \stdClass();
        
        if (isset($_GET['test'])){
        	echo '<pre>';
        	print_r($params);
        }
        
        $dat = $this->client->search($params);   // Execute the search
        
        $total = isset($dat['hits']['total']) ? $dat['hits']['total'] : 0;
        if (isset($dat['hits']['hits'])&&$dat['hits']['hits']){
            foreach ($dat['hits']['hits'] as $k=>$v){
                $data[$k]['id'] = $v['_id'];
                $data[$k]['type'] = $v['_type'];
                //$data[$k]['msg'] = isset($v['highlight']['msg'][0]) ? $v['highlight']['msg'][0]:$v['_source']['msg'];
                $data[$k]['msg'] = str_replace($keyword,'<em>'.$keyword.'</em>',$v['_source']['msg']);
                $data[$k]['ip'] = $v['_source']['ip'];
                $data[$k]['time'] = $v['_source']['time'];
                $data[$k]['addtime'] = isset($v['_source']['addtime'])?$v['_source']['addtime']:0;
                $data[$k]['level'] = $v['_source']['level'];
            }
        }
        $spend = isset($dat['took']) ? $dat['took'] : '';
        if (isset($_GET['test'])){
        	//echo '<pre>';
        	//print_r($params);
        }
        return array('total'=>$total,'list'=>$data,'spend'=>$spend);
    }
    public function delete_by($index,$type,$time_s,$time_e) //删除日志
    {
        if (!$index){
            throw new Exception('no index!');
        }
        $params['index'] = $index;
        if ($type){
            $params['type'] = $type;
        }
        if ($time_s){
            $params['body']['query']['range']['time']['gte'] = $time_s;
        }
        if ($time_e){
            $params['body']['query']['range']['time']['lte'] = $time_e;
        }
        //echo '<pre>';
        //print_r($params);
        return $this->client->deleteByQuery($params);
    }
}