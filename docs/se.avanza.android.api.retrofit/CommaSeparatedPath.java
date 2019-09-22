package se.avanza.android.api.retrofit;

import java.util.Iterator;
import kotlin.jvm.internal.h;

/* compiled from: CommaSeparatedPath.kt */
public final class CommaSeparatedPath<T> {
    public static final Companion Companion = new Companion(null);
    private static final String DELIMITER = ",";
    private final Iterable<T> collection;

    /* compiled from: CommaSeparatedPath.kt */
    public static final class Companion {
        private Companion() {
        }

        public /* synthetic */ Companion(DefaultConstructorMarker defaultConstructorMarker) {
            this();
        }
    }

    public CommaSeparatedPath(Iterable<? extends T> iterable) {
        h.b(iterable, "collection");
        this.collection = iterable;
    }

    public static /* synthetic */ CommaSeparatedPath copy$default(CommaSeparatedPath commaSeparatedPath, Iterable<T> iterable, int i2, Object obj) {
        if ((i2 & 1) != 0) {
            iterable = commaSeparatedPath.collection;
        }
        return commaSeparatedPath.copy(iterable);
    }

    public final Iterable<T> component1() {
        return this.collection;
    }

    public final CommaSeparatedPath<T> copy(Iterable<? extends T> iterable) {
        h.b(iterable, "collection");
        return new CommaSeparatedPath<>(iterable);
    }

    public boolean equals(Object obj) {
        return this == obj || ((obj instanceof CommaSeparatedPath) && h.a((Object) this.collection, (Object) ((CommaSeparatedPath) obj).collection));
    }

    public final Iterable<T> getCollection() {
        return this.collection;
    }

    public int hashCode() {
        Iterable<T> iterable = this.collection;
        if (iterable != null) {
            return iterable.hashCode();
        }
        return 0;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        Iterator<T> it = this.collection.iterator();
        while (it.hasNext()) {
            sb.append(it.next());
            if (it.hasNext()) {
                sb.append(DELIMITER);
            }
        }
        String sb2 = sb.toString();
        h.a((Object) sb2, "sb.toString()");
        return sb2;
    }
}
