$('.delete-cupcake').click(deleteCupcake)
$('#deleteButton').click(deleteCupcake)


async function deleteCupcake() {
    const id = $(this).data('id');
    await axios.delete(`/api/cupcakes/${id}`);
    $(this).parent().parent().remove()
}

$('#addCupcakeBtn').click(function() {
    location.href = "/cupcakes/add";
})

$('#returnButton').click(function() {
    location.href = "/";
})
