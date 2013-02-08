jQuery ->
    console.log('Script ran')
    $('#add-button').click (e) =>
        e.preventDefault()
        fields = [$('#input-title'), $('#input-text')]
        for field in fields
            if field.val().trim() == ""
                alert('Missing input')
                return

        postData =
            'title': fields[0].val()
            'note': fields[1].val()

        $.ajax
            url: '/stickies'
            type: 'POST'
            data: 'json': JSON.stringify(postData)
            success: (data) ->
                response = JSON.parse(data)
                id = response['id']
                title = response['title']
                note = response['note']
                html = $("
                    <div class='alert' data-id='#{id}'>
                    <button type='button' class='close' data-dismiss='alert'>&times;</button>
                    <h4>#{title}</h4>
                    <p>#{note}</p>
                    </div>")
                $('#stickies').prepend(html)
                html.hide().slideDown(500)
                html.children('button[class="close"]').click(deleteSticky)

    $('button[class="close"]').click(deleteSticky)
    

deleteSticky = (e) ->
    sticky = $(this).parent()
    sticky_id = sticky.attr('data-id')
    $.ajax
        url: '/delete'
        type: 'POST'
        data: 'id': sticky_id
        success: (data) ->
            if data == 'Success!'
                sticky.slideUp(500)