<?php
require_once("facebook.php");

// Create our Application instance (replace this with your appId and secret).
$facebook = new Facebook(array(
	'appId'  => 'yourAppID',
	'secret' => 'yourAppSecret',
	'fileUpload' => false, // optional
	'allowSignedRequest' => false, // optional, but should be set to false for non-canvas apps
));

$post_login = 'http://www.yourserver.com/getaccesstoken.php';

// Get User ID
$uid = $facebook->getUser();

// If the user is logged in and with permissions, let's move on and get the access token.
if(!empty($udid)){	
	header("Location: ". $post_login); 
} 
else 
{	
	$params = array(
		redirect_uri => $post_login,
		scope => 'read_stream,publish_stream'
	);
  $loginUrl = $facebook->getLoginUrl($params);
  
  header("Location: ". $loginUrl);
}
?>