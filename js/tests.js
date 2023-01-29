
function filter_data(elem){
    delete elem['image'];
    delete elem['color'];
    delete elem['alpha'];
    delete elem['index'];
    return elem;
}

function table_to_jsonl(source) {
    const subset = filter_data(source.data);
    const columns = Object.keys(subset)
    const nrows = source.get_length()
    let lines = ""
    
    for (let i = 0; i < nrows; i++) {
        let row = {};
        for (let j = 0; j < columns.length; j++) {
            const column = columns[j]
            row[column] = source.data[column][i]
        }
        lines = lines + JSON.stringify(row) + "\n"
    }
    return lines
}

function table_to_csv(source) {
    const subset = filter_data(source.data);
    const columns = Object.keys(subset)
    const nrows = source.get_length()
    const lines = [columns.join(',')]

    for (let i = 0; i < nrows; i++) {
        let row = [];
        for (let j = 0; j < columns.length; j++) {
            const column = columns[j]
            row.push(source.data[column][i].toString())
        }
        lines.push(row)
    }
    return lines.join('\n').concat('\n')
}


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
