<?php

require_once 'vendor/autoload.php';

class YouTubeSubtitleDownloader {
    private $client;
    private $youtube;
    private $videoId;

    public function __construct($clientSecretPath) {
        $this->client = new Google_Client();
        $this->client->setAuthConfig($clientSecretPath);
        $this->client->setScopes([
            'https://www.googleapis.com/auth/youtube.force-ssl',
            'https://www.googleapis.com/auth/youtube.readonly'
        ]);
        $this->client->setAccessType('offline');
        $this->client->setPrompt('consent');

        // Load previously authorized token, if it exists
        $tokenPath = 'token.json';
        if (file_exists($tokenPath)) {
            $accessToken = json_decode(file_get_contents($tokenPath), true);
            $this->client->setAccessToken($accessToken);
        }

        // If there is no previous token or it's expired.
        if ($this->client->isAccessTokenExpired()) {
            // Refresh the token if possible, else fetch a new one.
            if ($this->client->getRefreshToken()) {
                $this->client->fetchAccessTokenWithRefreshToken($this->client->getRefreshToken());
            } else {
                // Request authorization from the user.
                $authUrl = $this->client->createAuthUrl();
                printf("Open this link in your browser:\n%s\n", $authUrl);
                print 'Enter verification code: ';
                $authCode = trim(fgets(STDIN));

                // Exchange authorization code for an access token.
                $accessToken = $this->client->fetchAccessTokenWithAuthCode($authCode);
                $this->client->setAccessToken($accessToken);

                // Save the token to a file.
                if (!file_exists(dirname($tokenPath))) {
                    mkdir(dirname($tokenPath), 0700, true);
                }
                file_put_contents($tokenPath, json_encode($this->client->getAccessToken()));
            }
        }

        $this->youtube = new Google_Service_YouTube($this->client);
    }

    public function setVideoUrl($url) {
        $this->videoId = $this->extractVideoId($url);
        if (!$this->videoId) {
            throw new Exception('Invalid YouTube URL');
        }
        return $this;
    }

    private function extractVideoId($url) {
        $pattern = '/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})/i';
        if (preg_match($pattern, $url, $match)) {
            return $match[1];
        }
        return false;
    }

    public function getAvailableSubtitles() {
        $url = sprintf(
            'https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=%s&key=%s',
            $this->videoId,
            $this->apiKey
        );

        $response = $this->makeRequest($url);
        $data = json_decode($response, true);

        if (isset($data['error'])) {
            throw new Exception($data['error']['message']);
        }

        return $data['items'] ?? [];
    }

    public function downloadSubtitle($captionId, $format = 'srt') {
        $url = sprintf(
            'https://www.googleapis.com/youtube/v3/captions/%s?key=%s',
            $captionId,
            $this->apiKey
        );

        $headers = [
            'Authorization: Bearer ' . $this->apiKey
        ];

        if ($format === 'srt') {
            $headers[] = 'Accept: text/srt';
        } else {
            $headers[] = 'Accept: text/vtt';
        }

        return $this->makeRequest($url, $headers);
    }

    private function makeRequest($url, $headers = []) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpCode !== 200) {
            throw new Exception('Failed to fetch data from YouTube API');
        }

        return $response;
    }
}