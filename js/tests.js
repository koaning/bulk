
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
            const column = columns[j];
            const item = source.data[column][i];
            const value = typeof(item) == "string" ? '"' + item.toString() + '"' : item.toString()
            row.push(value);
        }
        lines.push(row);
    }
    return lines.join('\n').concat('\n')
}


var assert = require('assert');

describe('Super basic test', function () {
    it('should handle 1 == 1', function () {
        assert.equal(1, 1);
    });
});

describe('filter_data', function () {
    it('should handle throw out bad keys', function () {
        out = filter_data({"foo": 1, "image": 1})
        assert.equal("image" in out, false);
        assert.equal("color" in out, false);
        assert.equal("index" in out, false);
        assert.equal("alpha" in out, false);
    });
    it('should keep the right one', function () {
        out = filter_data({"foo": 1, "image": 1, "color": 1, "alpha": 1, "index": 1})
        assert.equal("foo" in out, true);
    });
});

describe('table-to-jsonl', function () {
    it('should handle base usage', function () {
        var data_in = {"data": {"text": ["this is text to keep"]}, "get_length": function(){return 1}}
        assert.equal(table_to_jsonl(data_in), '{"text":"this is text to keep"}\n');
    });
    it('should handle base usage with filter', function () {
        var data_in = {"data": {"text": ["this is text to keep"], "image": ["should be gone"]}, "get_length": function(){return 1}}
        assert.equal(table_to_jsonl(data_in), '{"text":"this is text to keep"}\n');
    });
    it('should handle base usage multiple rows', function () {
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

describe('table-to-csv', function () {
    it('should handle base usage', function () {
        var data_in = {"data": {"text": ["this is text to keep"]}, "get_length": function(){return 1}}
        assert.equal(table_to_csv(data_in), 'text\n"this is text to keep"\n');
    });
    it('should handle base usage multiple rows', function () {
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
        assert.equal(table_to_csv(data_in), 'text\n"this is text to keep"\n"so is this"\n');
    });
    it('should handle multiple columns', function () {
        var data_in = {
            "data": {
                "text": [
                    "this is text to keep", 
                    "so is this"
                ], 
                "meta": [
                    "should be kept", 
                    "this too"
                ]
            }, 
            "get_length": function(){return 2}
        }
        assert.equal(table_to_csv(data_in), 'text,meta\n"this is text to keep","should be kept"\n"so is this","this too"\n');
    });
    it('should handle nasty commas', function () {
        var data_in = {
            "data": {
                "text": [
                    "this is text, to keep", 
                    "so is this"
                ], 
                "meta": [
                    "should be kept", 
                    "this too"
                ]
            }, 
            "get_length": function(){return 2}
        }
        assert.equal(table_to_csv(data_in), 'text,meta\n"this is text, to keep","should be kept"\n"so is this","this too"\n');
    });
});
