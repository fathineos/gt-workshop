// Put the column heading above each field so the stacked mobile layout of the
// service inline is still readable. Works for rows added later too, because
// they are cloned from the hidden empty-form row.
window.addEventListener('load', function () {
    document.querySelectorAll('.js-inline-admin-formset table').forEach(function (table) {
        var labels = {};
        table.querySelectorAll('thead th[class*="column-"]').forEach(function (th) {
            var match = th.className.match(/column-(\S+)/);
            if (match) {
                labels[match[1]] = th.firstChild ? th.firstChild.textContent.trim() : '';
            }
        });

        table.querySelectorAll('tbody td[class*="field-"]').forEach(function (cell) {
            var match = cell.className.match(/field-(\S+)/);
            var text = match && labels[match[1]];
            if (!text || cell.querySelector('.mobile-label')) {
                return;
            }
            var label = document.createElement('label');
            label.className = 'mobile-label';
            label.textContent = text;
            cell.insertBefore(label, cell.firstChild);
        });
    });
});
