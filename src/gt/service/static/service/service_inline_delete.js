// Replace the "Delete?" checkbox of each saved service row with a Delete
// button. The button toggles the hidden checkbox, so the row is removed when
// the form is saved (and can still be restored with Undo before that).
window.addEventListener('load', function () {
    document.querySelectorAll('.js-inline-admin-formset tr.form-row.has_original').forEach(function (row) {
        var cell = row.querySelector('td.delete');
        var checkbox = cell && cell.querySelector('input[type=checkbox]');
        if (!checkbox) {
            return;
        }
        checkbox.classList.add('service-delete-checkbox');

        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'button service-delete-button';
        button.textContent = 'Delete';
        cell.appendChild(button);

        function sync() {
            row.classList.toggle('marked-for-delete', checkbox.checked);
            button.textContent = checkbox.checked ? 'Undo' : 'Delete';
        }
        button.addEventListener('click', function () {
            checkbox.checked = !checkbox.checked;
            sync();
        });
        sync();
    });
});
