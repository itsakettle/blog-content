class EndlessRecursion {

    public static void endlessRecursion(int x) {
        System.out.println("Depth: " + x);
        int y = 200;
        endlessRecursion(x+1);
    }

    public static void main(String[] args) {
        endlessRecursion(0);
    }
}