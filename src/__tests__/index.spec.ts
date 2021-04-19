import { createTestModel } from './utils';

import { TextTaggerModel } from '..';

describe('Example', () => {
  describe('ExampleModel', () => {
    it('should be createable', () => {
      const model = createTestModel(TextTaggerModel);
      expect(model).toBeInstanceOf(TextTaggerModel);
      expect(model.get('text')).toEqual('');
      expect(model.get('entity_spans')).toEqual([]);
      expect(model.get('classes')).toEqual([]);
      expect(model.get('palette')).toEqual([]);
      expect(model.get('selected_class')).toEqual('');
    });

    it('should be createable with a custom text', () => {
      const state = { text: 'Test text.' };
      const model = createTestModel(TextTaggerModel, state);
      expect(model).toBeInstanceOf(TextTaggerModel);
      expect(model.get('text')).toEqual('Test text.');
      expect(model.get('entity_spans')).toEqual([]);
    });

    it('should be createable with a custom classes', () => {
      const state = { text: 'Test text.', classes: ['hi', 'hello'] };
      const model = createTestModel(TextTaggerModel, state);
      expect(model).toBeInstanceOf(TextTaggerModel);
      expect(model.get('text')).toEqual('Test text.');
      expect(model.get('entity_spans')).toEqual([]);
      expect(model.get('classes')).toEqual(['hi', 'hello']);
    });
  });
});
