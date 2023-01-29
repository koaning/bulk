var assert = require('assert');

describe('Super basic test', function () {
    it('1 == 1', function () {
        assert.equal(1, 1);
    });
});

describe('filter_data', function () {
    it('throws out bad keys', function () {
        out = filter_data({"foo": 1, "image": 1})
        assert.equal("image" in out, false);
        assert.equal("color" in out, false);
        assert.equal("index" in out, false);
        assert.equal("alpha" in out, false);
    });
    it('keeps the right one', function () {
        out = filter_data({"foo": 1, "image": 1, "color": 1, "alpha": 1, "index": 1})
        assert.equal("foo" in out, true);
    });
});

describe('table-to-jsonl', function () {
    it('base usage', function () {
        var data_in = {"data": {"text": ["this is text to keep"]}, "get_length": function(){return 1}}
        assert.equal(table_to_jsonl(data_in), '{"text":"this is text to keep"}\n');
    });
    it('base usage with filter', function () {
        var data_in = {"data": {"text": ["this is text to keep"], "image": ["should be gone"]}, "get_length": function(){return 1}}
        assert.equal(table_to_jsonl(data_in), '{"text":"this is text to keep"}\n');
    });
    it('base usage multiple rows', function () {
        var data_in = {
            "data": {
                "text": [
                    "this is text to keep", 
                    "so is this"
                ], 
                "image": [
                    "should be gone", 
                    "this too"
                ]
            }, 
            "get_length": function(){return 2}
        }
        assert.equal(table_to_jsonl(data_in), '{"text":"this is text to keep"}\n{"text":"so is this"}\n');
    });
});
