from app.base.base_module import BaseModule
from app.modules.ocr.ocr_ctc.ocr_ctc_model import OcrCtcModel


class OcrHW(BaseModule):

    def __init__(self):
        BaseModule.__init__(self)
        data_path = self.get_model_path('ocr_ctc/data.json')
        vocab_path = self.get_model_path('ocr_ctc/vocab.json')
        model_path = self.get_model_path('ocr_ctc/model.json')
        model_weight = self.get_model_path('ocr_ctc/model.weights')
        # dir_output = self.afw_debug.get_output_dir()
        dir_output = self.get_model_path('ocr_ctc/')
        self.afw_logging.info("{} - LOAD MODELS: {}".format(self.class_name, model_weight))
        self.model = OcrCtcModel()
        self.model.load_models(data_path, vocab_path, model_path, model_weight, dir_output)

    def process(self, kwargs):
        self.afw_logging.info("{} - PROCESSING...".format(self.class_name))
        img = kwargs.get('img')
        if isinstance(img, str):
            img = self.imread(img)

        kwargs['value'] = ''
        kwargs['confidence_score_by_field'] = 0
        try:
            if self.model is not None and img is not None:
                results, confidence_score = self.model.predict(img)
                kwargs['value'] = results[0]
                kwargs['confidence_score_by_field'] = confidence_score[0]
        except:
            self.afw_logging.exception()

        return kwargs
