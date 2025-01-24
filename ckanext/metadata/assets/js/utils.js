function delete_flash(flash) {
    console.log(flash)
    $(flash).parent().remove()
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('metadata_delete_form').addEventListener('submit', async function(event) {
        event.preventDefault();
        const metadataId = document.getElementById('metadata_delete_id').value
        console.log(metadataId)
        const url_delete = document.getElementById('metadata_delete_url').value
        console.log(url_delete)

        messageElement = '';

        try {
        const response = await fetch(url_delete, {
            method: 'DELETE',
        });

        if(response.ok) {
            const result = await response.json();
            console.log(result)

            messageElement = `Message: ${result.message}`;
        } 
        else {
            const error = await response.json();
           messageElement = `Error: ${error.error || 'Failed to delete metadata'}`;
        }

        }
        catch(error) {
        messageElement = `Error: ${error.message || 'An unexpected error occurred'}`; 
        }
    });
})