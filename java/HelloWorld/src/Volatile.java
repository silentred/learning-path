public class Volatile {

    public static int count = 0;

    public static void inc() {
        try {
           Thread.sleep(1);
        } catch (InterruptedException e) {
            
        }
        count++;
    }

   public static void main(String[] args) {
       for (int i = 0; i < 1000; i++) {
           new Thread(new Runnable() {
               @Override
               public void run() {
                   Volatile.inc();
               }
           }).start();
       }
       //需要等待thread全部完成后再打印计数
       System.out.println("运行结果:Counter.count=" + Volatile.count);
   }
}
