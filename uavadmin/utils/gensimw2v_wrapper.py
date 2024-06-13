import logging

# from gensim.models import word2vec

from appuav.settings import AI_CONF

logger = logging.getLogger(__name__)

w2v_model = None


def calc_top10(q):
    if not w2v_model:
        w2v_model = word2vec.Word2Vec.load(AI_CONF["gensim_w2v_model"])
    sims = w2v_model.wv.most_similar(q)
    logger.info(f"q={q} sims={sims}")
    return sims
