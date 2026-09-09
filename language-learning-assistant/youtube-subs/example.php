<?php

require_once 'YouTubeSubtitleDownloader.php';

try {
    $clientSecretPath = 'client_secret_211119282460-h1fnalspiev0u6dq983bkkq6t8fhrqg6.apps.googleusercontent.com.json';
    $downloader = new YouTubeSubtitleDownloader($clientSecretPath);
    
    // Example YouTube video URL
    $videoUrl = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
    
    // Set the video URL and get available subtitles
    $subtitles = $downloader->setVideoUrl($videoUrl)->getAvailableSubtitles();

    if (empty($subtitles)) {
        echo "No subtitles available for this video.\n";
        exit;
    }

    echo "Available subtitles:\n";
    foreach ($subtitles as $subtitle) {
        echo sprintf(
            "Language: %s, Track Name: %s\n",
            $subtitle['snippet']['language'],
            $subtitle['snippet']['name']
        );
    }

    // Download the first available subtitle in SRT format
    $firstSubtitle = $subtitles[0];
    $subtitleContent = $downloader->downloadSubtitle($firstSubtitle['id'], 'srt');

    // Save the subtitle to a file
    $filename = sprintf('subtitle_%s_%s.srt', 
        $firstSubtitle['snippet']['language'],
        date('Y-m-d_His')
    );
    file_put_contents($filename, $subtitleContent);
    
    echo "\nSubtitle downloaded successfully: {$filename}\n";

} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}