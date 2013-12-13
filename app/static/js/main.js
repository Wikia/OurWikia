/**
jQuery(document).ready(function() {
    var csrf = jQuery('input[name="csrfmiddlewaretoken"]').val();
    jQuery('.voters a').click(function(e) {
        var self = $(this);

        if (self.hasClass('nag')) {
            $('#nagModal').modal('show')
            jQuery.alert("Please log in or sign up to vote on stories");

        } else {
            var story_id = $(this).data('id');
            var params = {'csrfmiddlewaretoken': csrf};
            var vote_type = 'upvote';
            var delta = 0;
            if (self.hasClass('downvote')) {
                vote_type = 'downvote';
                delta = -1;
                if (self.hasClass('active')) {
                    params['delete'] = 1;
                    delta += 2;
                } else if (self.closest('.voters').find('.upvote.active').length > 0) {
                    self.closest('.voters').find('.upvote.active').toggleClass('active');
                    delta -= 1;
                }
            }
            if (self.hasClass('upvote')) {
                vote_type = 'upvote';
                delta = 1;
                if (self.hasClass('active')) {
                    params['delete'] = 1;
                    delta -= 2;
                } else if (self.closest('.voters').find('.downvote.active').length > 0) {
                    self.closest('.voters').find('.upvote.active').toggleClass('active');
                    delta += 1;
                }
            }

            self.toggleClass('active');
            jQuery.post('/'+story_id+'/'+vote_type+'/', params, function() {
                var scorespan = self.closest('.voters').find('.score-number');
                scorespan.text(parseInt(scorespan.text())+delta);
            });
        }
        e.stopPropagation();
        return false;
    })
});
**/