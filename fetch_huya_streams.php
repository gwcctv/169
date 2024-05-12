<?php
error_reporting(0);
set_time_limit(600);

function get_data($url)
{
    $ch = curl_init();
    $User_Agent = 'Mozilla/5.0 (Linux; U; Android 4.0.4; zh-cn; HTC T528w Build/IMM76D) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025410  Safari/533.1';
    $timeout = 5;
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_ENCODING, '');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_USERAGENT, $User_Agent);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('X-FORWARDED-FOR:' . $_SERVER['REMOTE_ADDR'], 'CLIENT-IP:' . $_SERVER['REMOTE_ADDR']));
    $chr = curl_exec($ch);
    curl_close($ch);
    return $chr;
}

$huya_streams = '';

// Fetch Huya streams for "huya一起看-电影"
$huya_streams .= "huya一起看-电影" . "\n";
$str = json_decode(get_data('https://live.huya.com/liveHttpUI/getTmpLiveList?iTmpId=2067&iPageNo=1&iPageSize=120&iLibId=2213&iGid=2135'), 1);
foreach ($str['vList'] as $v) {
    $id = $v['lProfileRoom'];
    $name = $v['sIntroduction'];
    $d = get_data('https://m.huya.com/' . $id);
    preg_match('/"sStreamName":"(.*?)"/', $d, $sStreamName);
    $m3u8 = "http://43.137.29.240/tx.flv.huya.com/src/" . $sStreamName[1] . ".m3u8";
    $huya_streams .= $name . "," . $m3u8 . "\n";
}

// Fetch Huya streams for "huya一起看-TVB"
$huya_streams .= "huya一起看-TVB" . "\n";
$str = json_decode(get_data('https://live.huya.com/liveHttpUI/getTmpLiveList?iTmpId=4061&iPageNo=1&iPageSize=120&iLibId=4149&iGid=2135'), 1);
foreach ($str['vList'] as $v) {
    $id = $v['lProfileRoom'];
    $name = $v['sIntroduction'];
    $d = get_data('https://m.huya.com/' . $id);
    preg_match('/"sStreamName":"(.*?)"/', $d, $sStreamName);
    $m3u8 = "http://43.137.29.240/tx.flv.huya.com/src/" . $sStreamName[1] . ".m3u8";
    $huya_streams .= $name . "," . $m3u8 . "\n";
}

// Save the streams to a file
file_put_contents('huya_streams.txt', $huya_streams);
?>
