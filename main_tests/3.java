
class A {
    static int x;
    static int y;
    static int z;

    public static int set(int val) {
        int k;
        k = val;
        x = k;
        y = k;
        z = k;
        return val;
    }
}

class B extends A {
    static int y;
    static int z;

    public static int set(int val) {
        int k;
        k = val;
        y = k;
        z = k;
        return y;
    }
}

class C extends B {
    static int z;

    public static int set(int val) {
        int k;
        k = val;
        z = k;
        return z;
    }
}

public class Main {
    public static void main( ) {
        System.out.println(A.set(1));
        System.out.println(B.set(2));
        System.out.println(C.set(3));
        System.out.println(A.x);
        System.out.println(A.y);
        System.out.println(A.z);
        System.out.println(B.x);
        System.out.println(B.y);
        System.out.println(B.z);
        System.out.println(C.x);
        System.out.println(C.y);
        System.out.println(C.z);
    }
}
EOF