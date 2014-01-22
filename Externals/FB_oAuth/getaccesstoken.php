<?php
require_once("facebook.php");

//instantiate the Facebook library with the APP ID and APP SECRET
$facebook = new Facebook(array(
	'appId'  => 'yourAppID',
	'secret' => 'yourAppSecret',
	'fileUpload' => false, // optional
	'allowSignedRequest' => false, // optional, but should be set to false for non-canvas apps
));

$user = $facebook->getUser();

if ($user) {	
	$access_token = $facebook->getAccessToken();
	// Pass over the access token back to our python webserver to be caught by the BaseHTTPRequestHandler and stored
	header("Location: http://127.0.0.1?access_token=". $access_token);
}
?>