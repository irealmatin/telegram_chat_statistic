from typing import Union # type annotation
from pathlib import Path
import json
from src.data import DATA_DIR
from hazm import word_tokenize , Normalizer
from wordcloud import WordCloud
import arabic_reshaper
from bidi.algorithm import get_display
from loguru import logger


class ChatStatistic :
    """generate chat statistic from telegram chat json file
    """
    def __init__(self , chat_json : Union[str , Path]) :
        """
        :param chat_json : path to telegram export json file
        """
        #load chat data
        logger.info(f"loading chat data from {chat_json}")
        with open(chat_json) as f :
            self.chat_data = json.load(f)

        self.normalizer = Normalizer()

        # load stop words
        stopwords = open(DATA_DIR / "persian_stop_words.txt").readlines()
        stopwords = list(map(str.strip , stopwords))
        self.stopwords = list(map(self.normalizer.normalize , stopwords))

    def generate_wordcloud(self , output_dir : Union[str ,Path]):
        """generate a word cloud from chat data
        """
        txt_content = ''
        
        logger.info("Generating word cloud ...")
        for msg in self.chat_data["messages"] :
            if type(msg["text"]) is str :
                tokens = word_tokenize(msg["text"])
                tokens = list(filter(lambda item : item not in self.stopwords , tokens))
                
                txt_content += f" {' '.join(tokens)}" # for show better 

        # normalize , reshape wordcloud
        logger.info("in stage of normalizing and reshaping ...")
        txt_content = self.normalizer.normalize(txt_content)
        txt_content = arabic_reshaper.reshape(txt_content)
        txt_content = get_display(txt_content)

        
        word_cloud = WordCloud(font_path =str(DATA_DIR / 'Bhomafont.ttf' ) ,
                                width = 1100 ,
                                height = 1100 ).generate(txt_content)
        logger.info(f"Saving word cloud to {output_dir}")

        word_cloud.to_file(str(Path(output_dir / 'wordcloud.png')))

if  __name__ == "__main__":
    chat_stats = ChatStatistic(chat_json=DATA_DIR / 'result.json')
    chat_stats.generate_wordcloud(output_dir=DATA_DIR)

    print("Done!")

