(function() {

    // Vars.
    var $form = document.querySelectorAll('#mc-embedded-subscribe-form')[0],
        $submit = document.querySelectorAll('#mc-embedded-subscribe-form input[type="submit"]')[0],
        $message;

    // Bail if addEventListener isn't supported.
    if (!('addEventListener' in $form))
        return;

    // Message.
    $message = document.createElement('div');
    $message.classList.add('response');
    $form.appendChild($message);

    $message._show = function(type, text) {

        $message.innerHTML = text;
        $message.classList.add(type);
        $message.classList.add('visible');

        window.setTimeout(function() {
            $message._hide();
        }, 3000);

    };

    $message._hide = function() {
        $message.classList.remove('visible');
    };

    // Events.
    // Note: If you're *not* using AJAX, get rid of this event listener.
    $form.addEventListener('submit', function(event) {

        event.stopPropagation();
        event.preventDefault();

        // Hide message.
        $message._hide();

        // Disable submit.
        $submit.disabled = true;

        // Process form.
        // Note: Doesn't actually do anything yet (other than report back with a "thank you"),
        // but there's enough here to piece together a working AJAX submission call that does.
        window.setTimeout(function() {
            
            var msg   = $('#mc-embedded-subscribe-form').serialize();
            $.ajax({
                type: 'POST',
                url: 'send.php',
                data: msg,
                success: function(data) {
                    $('#mce-responses').html(data);
                },
                error:  function(xhr, str){
                    alert('Error: ' + xhr.responseCode);
                }
            });

            // Reset form.
            $form.reset();

            // Enable submit.
            $submit.disabled = false;

        }, 750);

    });

})();