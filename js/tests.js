
function table_to_csv(source) {
    const subset_col = ["text", "path"].filter(_ => source.data[_])[0];
    let subset = {};
    subset[subset_col] = source.data[subset_col]
    console.log(subset_col, subset);
    const columns = Object.keys(subset)
    const nrows = source.get_length()
    const lines = [columns.join(',')]

    for (let i = 0; i < nrows; i++) {
        let row = [];
        for (let j = 0; j < columns.length; j++) {
            const column = columns[j]
            console.log(column, source.data);
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
