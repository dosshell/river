package se.avanza.android.api.retrofit;

import io.reactivex.Completable;
import io.reactivex.Observable;
import io.reactivex.Single;
import java.util.List;
import okhttp3.e0;
import retrofit2.t.a;
import retrofit2.t.b;
import retrofit2.t.e;
import retrofit2.t.j;
import retrofit2.t.m;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.models.messages.AttachmentConstraints;
import se.avanza.android.api.models.messages.Message;
import se.avanza.android.api.models.messages.MessageCategory;
import se.avanza.android.api.models.messages.MessageId;
import se.avanza.android.api.models.messages.MessageSendRequest;
import se.avanza.android.api.models.messages.MessageText;
import se.avanza.android.api.models.messages.UnreadCount;

/* compiled from: MessageApi.kt */
public interface MessageApi {

    /* compiled from: MessageApi.kt */
    public static final class DefaultImpls {
        @e("/_mobile/customer/message/conversations")
        public static /* synthetic */ Single getConversations$default(MessageApi messageApi, int i2, int i3, int i4, int i5, Object obj) {
            if (obj == null) {
                if ((i5 & 4) != 0) {
                    i4 = 200;
                }
                return messageApi.getConversations(i2, i3, i4);
            }
            throw new UnsupportedOperationException("Super calls with default arguments not supported in this target, function: getConversations");
        }
    }

    @e("/_mobile/customer/attachment-constraints")
    Single<AttachmentConstraints> attachmentConstraints();

    @e("/_mobile/customer/message/category")
    Single<List<MessageCategory>> categories();

    @b("/_mobile/customer/message/conversation/{messageId}")
    Completable deleteConversation(@q("messageId") MessageId messageId);

    @e("/_mobile/customer/message-attached-file/{messageId}/{documentId}")
    Observable<e0> getAttachment(@q("messageId") MessageId messageId, @q("documentId") String str);

    @e("/_mobile/customer/message/conversation/{messageId}")
    @j({"AZA-Accept-Formatting: text/markdown"})
    Single<List<Message>> getConversation(@q("messageId") MessageId messageId);

    @e("/_mobile/customer/message/conversations")
    Single<List<Message>> getConversations(@r("conversationIndex") int i2, @r("listSize") int i3, @r("previewSize") int i4);

    @m("/_mobile/customer/message/{messageBox}/{messageId}/read")
    Completable markMessageAsRead(@q("messageBox") String str, @q("messageId") MessageId messageId);

    @m("/_mobile/customer/message/{messageId}/reply")
    Single<MessageId> replyMessage(@q("messageId") MessageId messageId, @a MessageText messageText);

    @m("/_mobile/customer/message")
    Completable sendMessage(@a MessageSendRequest messageSendRequest);

    @e("/_mobile/customer/message/unreadcount/Inbox")
    Single<UnreadCount> unreadMessageCount();
}
