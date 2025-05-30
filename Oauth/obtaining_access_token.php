<?php

require_once 'defines.php';
require_once __DIR__ . '/vendor/autoload.php';
$creds = array(
    'app_id' => FACEBOOK_APP_ID,
    'app_secret' => FACEBOOK_APP_SECRET,
    'default_graph_version' => 'v22.0',
    'persistent_data_handler' => 'session'
);


$facebook = new Facebook\Facebook($creds);


$helper = $facebook->getRedirectLoginHelper();



$oAuth2Client = $facebook->getOAuth2Client();

if(isset($_GET['code'])){
    try{
        $accessToken = $helper->getAccessToken();
    }
    catch(Facebook\Exceptions\FacebookResponseException $e){
        echo 'Graph returned an error: ' . $e->getMessage();
    }
}
else{
    $permissions = ['public_profile', 'instagram_basic', 'pages_show_list'];
    $loginUrl = $helper->getLoginUrl(FACEBOOK_REDIRECT_URI, $permissions);
    echo '<a href="' . $loginUrl . '">Login With Facebook</a>';
    echo 'hello';

    


}





?>