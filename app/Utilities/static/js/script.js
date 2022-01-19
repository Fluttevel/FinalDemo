function delete_question(cr_number)
{
    if (confirm("Вы уверены?"))
    {
        document.getElementById('delete_data_form_' + String(cr_number)).submit()
    }
}