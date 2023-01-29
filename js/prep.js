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
