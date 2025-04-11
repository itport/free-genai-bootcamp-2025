/**
 * Japanese vocabulary for the language immersion game
 * Each word includes:
 * - japanese: The Japanese word
 * - romaji: Romanized Japanese
 * - english: English translation
 * - partOfSpeech: Type of word (noun, verb, adjective, etc.)
 * - context: Example usage in a sentence
 * - difficulty: 1-5 scale (1 = beginner, 5 = advanced)
 */

export const vocabulary = [
  // Nouns
  {
    japanese: "家",
    romaji: "ie",
    english: "house",
    partOfSpeech: "noun",
    context: "これは私の家です。(Kore wa watashi no ie desu.)",
    difficulty: 1
  },
  {
    japanese: "テーブル",
    romaji: "tēburu",
    english: "table",
    partOfSpeech: "noun",
    context: "本はテーブルの上にあります。(Hon wa tēburu no ue ni arimasu.)",
    difficulty: 1
  },
  {
    japanese: "本",
    romaji: "hon",
    english: "book",
    partOfSpeech: "noun",
    context: "私は本を読むのが好きです。(Watashi wa hon o yomu no ga suki desu.)",
    difficulty: 1
  },
  {
    japanese: "鍵",
    romaji: "kagi",
    english: "key",
    partOfSpeech: "noun",
    context: "家の鍵をなくしました。(Ie no kagi o nakushimashita.)",
    difficulty: 1
  },
  {
    japanese: "ドア",
    romaji: "doa",
    english: "door",
    partOfSpeech: "noun",
    context: "ドアは閉まっています。(Doa wa shimatte imasu.)",
    difficulty: 1
  },
  {
    japanese: "窓",
    romaji: "mado",
    english: "window",
    partOfSpeech: "noun",
    context: "窓を開けてください。(Mado o akete kudasai.)",
    difficulty: 1
  },
  {
    japanese: "水",
    romaji: "mizu",
    english: "water",
    partOfSpeech: "noun",
    context: "水を飲みたいです。(Mizu o nomitai desu.)",
    difficulty: 1
  },
  {
    japanese: "パン",
    romaji: "pan",
    english: "bread",
    partOfSpeech: "noun",
    context: "私は新鮮なパンが好きです。(Watashi wa shinsen na pan ga suki desu.)",
    difficulty: 1
  },
  {
    japanese: "椅子",
    romaji: "isu",
    english: "chair",
    partOfSpeech: "noun",
    context: "椅子に座っています。(Isu ni suwatte imasu.)",
    difficulty: 1
  },
  {
    japanese: "ベッド",
    romaji: "beddo",
    english: "bed",
    partOfSpeech: "noun",
    context: "ベッドで寝ます。(Beddo de nemasu.)",
    difficulty: 1
  },

  // Adjectives
  {
    japanese: "大きい",
    romaji: "ōkii",
    english: "big",
    partOfSpeech: "adjective",
    context: "家は大きいです。(Ie wa ōkii desu.)",
    difficulty: 1
  },
  {
    japanese: "小さい",
    romaji: "chiisai",
    english: "small",
    partOfSpeech: "adjective",
    context: "鍵は小さいです。(Kagi wa chiisai desu.)",
    difficulty: 1
  },
  {
    japanese: "古い",
    romaji: "furui",
    english: "old",
    partOfSpeech: "adjective",
    context: "本は古いです。(Hon wa furui desu.)",
    difficulty: 1
  },
  {
    japanese: "新しい",
    romaji: "atarashii",
    english: "new",
    partOfSpeech: "adjective",
    context: "椅子は新しいです。(Isu wa atarashii desu.)",
    difficulty: 1
  },
  {
    japanese: "開いている",
    romaji: "aite iru",
    english: "open",
    partOfSpeech: "adjective",
    context: "窓は開いています。(Mado wa aite imasu.)",
    difficulty: 1
  },
  {
    japanese: "閉まっている",
    romaji: "shimatte iru",
    english: "closed",
    partOfSpeech: "adjective",
    context: "ドアは閉まっています。(Doa wa shimatte imasu.)",
    difficulty: 1
  },

  // Verbs (dictionary form)
  {
    japanese: "行く",
    romaji: "iku",
    english: "to go",
    partOfSpeech: "verb",
    context: "家に行きたいです。(Ie ni ikitai desu.)",
    difficulty: 1
  },
  {
    japanese: "取る",
    romaji: "toru",
    english: "to take",
    partOfSpeech: "verb",
    context: "本を取ってもいいですか？(Hon o totte mo ii desu ka?)",
    difficulty: 1
  },
  {
    japanese: "見る",
    romaji: "miru",
    english: "to see",
    partOfSpeech: "verb",
    context: "家を見ることができます。(Ie o miru koto ga dekimasu.)",
    difficulty: 1
  },
  {
    japanese: "開ける",
    romaji: "akeru",
    english: "to open",
    partOfSpeech: "verb",
    context: "ドアを開けたいです。(Doa o aketai desu.)",
    difficulty: 1
  },
  {
    japanese: "閉める",
    romaji: "shimeru",
    english: "to close",
    partOfSpeech: "verb",
    context: "窓を閉める必要があります。(Mado o shimeru hitsuyoō ga arimasu.)",
    difficulty: 1
  },
  {
    japanese: "食べる",
    romaji: "taberu",
    english: "to eat",
    partOfSpeech: "verb",
    context: "パンを食べたいです。(Pan o tabetai desu.)",
    difficulty: 1
  },
  {
    japanese: "飲む",
    romaji: "nomu",
    english: "to drink",
    partOfSpeech: "verb",
    context: "水を飲みたいです。(Mizu o nomitai desu.)",
    difficulty: 1
  },
  {
    japanese: "話す",
    romaji: "hanasu",
    english: "to speak",
    partOfSpeech: "verb",
    context: "日本語を話すことができます。(Nihongo o hanasu koto ga dekimasu.)",
    difficulty: 1
  },
  {
    japanese: "あげる",
    romaji: "ageru",
    english: "to give",
    partOfSpeech: "verb",
    context: "本をあげたいです。(Hon o agetai desu.)",
    difficulty: 1
  },
  {
    japanese: "使う",
    romaji: "tsukau",
    english: "to use",
    partOfSpeech: "verb",
    context: "鍵を使ってもいいですか？(Kagi o tsukatte mo ii desu ka?)",
    difficulty: 1
  }
];

// Helper function to get a random word from the vocabulary
export const getRandomWord = (partOfSpeech = null, difficulty = null) => {
  let filteredWords = [...vocabulary];

  if (partOfSpeech) {
    filteredWords = filteredWords.filter(word => word.partOfSpeech === partOfSpeech);
  }

  if (difficulty) {
    filteredWords = filteredWords.filter(word => word.difficulty === difficulty);
  }

  const randomIndex = Math.floor(Math.random() * filteredWords.length);
  return filteredWords[randomIndex];
};

// Helper function to find a word by its Japanese text or romaji
export const findWordByJapanese = (japaneseWord) => {
  return vocabulary.find(word => word.japanese === japaneseWord || word.romaji.toLowerCase() === japaneseWord.toLowerCase());
};

// Helper function to find a word by its English text
export const findWordByEnglish = (englishWord) => {
  return vocabulary.find(word => word.english.toLowerCase() === englishWord.toLowerCase());
};
