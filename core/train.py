import click
import os

from core.model.utils.data_generator import DataGenerator
# from model.img2seq import Img2SeqModel
from core.model.img2seq_ctc import Img2SeqCtcModel
from core.model.utils.lr_schedule import LRSchedule
from core.model.utils.text import Vocab
from core.model.utils.image import greyscale
from core.utility.md_config import MdConfig


@click.command()
@click.option('--data', default="configs/data.json",
              help='Path to data json config')
@click.option('--vocab', default="configs/vocab.json",
              help='Path to vocab json config')
@click.option('--training', default="configs/training.json",
              help='Path to training json config')
@click.option('--log', default="configs/log.json",
              help='Path to log json config')
@click.option('--dir_output', default="data/output/model/",
              help='Dir for results and model weights')
@click.option('--restore', default=False,
              help='Resume training from model weights')
def main(data, vocab, training, log, dir_output, restore):
    # Load configs
    config = MdConfig([data, vocab, training, log])
    # config.dict_json

    dir_output = config.get_root_path(dir_output)
    config.save(dir_output)
    config.dir_output = dir_output
    vocab = Vocab(config)

    # Load datasets
    train_set = DataGenerator(path_formulas=config.get_path('path_formulas_train', 'D'),
                              dir_images=config.get_path('dir_images_train', 'D'), img_prepro=greyscale,
                              max_iter=config.max_iter, bucket=config.bucket_train,
                              path_matching=config.get_path('path_matching_train', 'D'),
                              max_len=config.max_length_formula,
                              form_prepro=vocab.form_prepro)

    val_set = DataGenerator(path_formulas=config.get_path('path_formulas_val', 'D'),
                            dir_images=config.get_path('dir_images_val', 'D'), img_prepro=greyscale,
                            max_iter=config.max_iter, bucket=config.bucket_val,
                            path_matching=config.get_path('path_matching_val', 'D'),
                            max_len=config.max_length_formula,
                            form_prepro=vocab.form_prepro)

    # Define learning rate schedule
    n_batches_epoch = ((len(train_set) + config.batch_size - 1) / config.batch_size)
    lr_schedule = LRSchedule(lr_init=config.lr_init,
                             start_decay=config.start_decay * n_batches_epoch,
                             end_decay=config.end_decay * n_batches_epoch,
                             end_warm=config.end_warm * n_batches_epoch,
                             lr_warm=config.lr_warm,
                             lr_min=config.lr_min)

    # Build model and train
    model = Img2SeqCtcModel(config)
    model.build_train()

    if restore:
        model.restore_session()

    model.train(config, train_set, val_set, lr_schedule)


if __name__ == "__main__":
    main()
