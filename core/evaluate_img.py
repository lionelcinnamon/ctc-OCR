import click

from core.model.utils.data_generator import DataGenerator
from core.model.img2seq import Img2SeqModel
from core.utility.md_config import MdConfig
from core.model.utils.text import Vocab, load_formulas
from core.model.utils.image import greyscale, build_images
from core.model.img2seq_ctc import Img2SeqCtcModel

from core.model.evaluation.text import score_files
from core.model.evaluation.image import score_dirs


@click.command()
@click.option('--results', default="data/output/model/", help='Dir to results')
def main(results):
    # restore config and model
    dir_output = results

    config = MdConfig(["data/output/model/data.json", "data/output/model/vocab.json", "data/output/model/model.json"])
    config.show_json
    model = Img2SeqCtcModel(config)
    model.build_pred()
    model.restore_session()
    vocab = Vocab(config)

    # load dataset
    test_set = DataGenerator(path_formulas=config.get_path('path_formulas_test', 'D'),
                             dir_images=config.get_path('dir_images_test', 'D'), img_prepro=greyscale,
                             max_iter=config.get('max_iter'), bucket=config.get('bucket_test'),
                             path_matching=config.get_path('path_matching_test', 'D'),
                             max_len=config.get('max_length_formula'),
                             form_prepro=vocab.form_prepro, )

    # build images from formulas
    formula_ref = dir_output + "formulas_test/ref.txt"
    formula_hyp = dir_output + "formulas_test/hyp_0.txt"
    images_ref = dir_output + "images_test/ref/"
    images_test = dir_output + "images_test/hyp_0/"
    build_images(load_formulas(formula_ref), images_ref)
    build_images(load_formulas(formula_hyp), images_test)

    # score the repositories
    scores = score_dirs(images_ref, images_test, greyscale)
    msg = " - ".join(["{} {:04.2f}".format(k, v) for k, v in scores.items()])
    model.logger.info("- Eval Img: {}".format(msg))


if __name__ == "__main__":
    main()
