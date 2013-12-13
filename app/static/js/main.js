jQuery(document).ready(function() {
    jQuery('.voters a').click(function(e) {
        var self = $(this);

        if (self.hasClass('nag')) {
            $('#nagModal').modal('show')
            jQuery.alert("Please log in or sign up to vote on stories");

        } else {
            var story_id = $(this).data('id');
            var params = {};
            var vote_type = 'upvote';
            if (self.hasClass('downvote')) {
                vote_type = 'downvote';
            }
            if (self.hasClass('active')) {
                params['delete'] = 1;
            }
            self.toggleClass('active');
            jQuery.post('/'+story_id+'/'+vote_type+'/', params, function() {

            });
        }
        e.stopPropagation();
        return false;
    })
});