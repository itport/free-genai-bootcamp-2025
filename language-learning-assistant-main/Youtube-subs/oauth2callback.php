<?php
require_once 'vendor/autoload.php';

try {
    $client = new Google_Client();
    $client->setAuthConfig('client_secret_211119282460-h1fnalspiev0u6dq983bkkq6t8fhrqg6.apps.googleusercontent.com.json');
    
    // Store the code from Google
    if (isset($_GET['code'])) {
        $token = $client->fetchAccessTokenWithAuthCode($_GET['code']);
        file_put_contents('token.json', json_encode($token));
        echo "Authorization successful! Please close this window and restart the script.";
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}