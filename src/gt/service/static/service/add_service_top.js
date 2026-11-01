// Show the inline "Add another" button above the service list and insert new
// entries at the top, matching the newest-first ordering of the list.
window.addEventListener('load', function () {
    document.querySelectorAll('.js-inline-admin-formset').forEach(function (group) {
        var addRow = group.querySelector('tr.add-row');
        var addLink = addRow && addRow.querySelector('a');
        var table = group.querySelector('table');
        if (!addLink || !table) {
            return;
        }

        // Reuse the original link so Django's click handler keeps working.
        var wrapper = document.createElement('div');
        wrapper.className = 'add-row';
        wrapper.appendChild(addLink);
        table.parentNode.insertBefore(wrapper, table);
        addRow.style.display = 'none';

        addLink.addEventListener('click', function () {
            // Django inserts the new row just before the hidden empty-form
            // template row; move it up.
            var template = table.querySelector('tbody tr.empty-form');
            var newRow = template && template.previousElementSibling;
            var firstRow = table.querySelector('tbody tr.form-row:not(.empty-form)');
            if (newRow && firstRow && newRow !== firstRow) {
                firstRow.parentNode.insertBefore(newRow, firstRow);
            }
        });
    });
});
