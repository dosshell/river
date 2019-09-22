package se.avanza.android.api.retrofit;

import io.reactivex.Single;
import java.util.List;
import retrofit2.t.e;
import retrofit2.t.q;
import retrofit2.t.r;
import se.avanza.android.api.models.forum.ForumPost;

/* compiled from: ForumApi.kt */
public interface ForumApi {
    @e("/_mobile/forum/post/company/{companyId}")
    Single<List<ForumPost>> getCompanyForumPosts(@q("companyId") String str, @r("start") int i2, @r("limit") int i3);
}
