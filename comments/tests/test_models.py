from comments.models import Comment


def test_create_comment_reply(product_db, user_db):
    comment = Comment.objects.create(
        product=product_db,
        author=user_db,
        content="Test comment"
    )

    reply = Comment.objects.create(
        product=product_db,
        author=user_db,
        content="Reply comment",
        parent_comment=comment,
    )

    parent_com = Comment.objects.first()
    reply_comment = Comment.objects.filter(parent_comment__isnull=False).first()

    assert parent_com.replies.first() == reply
    assert reply_comment.parent_comment == parent_com
