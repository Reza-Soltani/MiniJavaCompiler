class A {
    static int x;
    public static int y(int y) {
        return y * 2;
    }
}

class B extends A{
    public static int y(int y) {
        return y * 2;
    }
}

class C extends B{
    public static int y(int y) {
        return y * 2;
    }
}

class D extends C{
    public static int y(int y) {
        x = 10;
        return y * 2;
    }
}

class E {
    public static int y(int y) {
        return y * 2;
    }
}

public class Main {
    public static void main( ) {
        int x;
        System.out.println(D.y(3));
        System.out.println(A.x);
    }
}
EOF