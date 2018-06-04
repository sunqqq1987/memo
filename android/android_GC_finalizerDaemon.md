
# 错误log #

	<6>[124702.625273]  [0:FinalizerWatchd: 1373] *** FATAL EXCEPTION IN SYSTEM PROCESS: FinalizerWatchdogDaemon
	<6>[124702.625273]  [0:FinalizerWatchd: 1373] java.util.concurrent.TimeoutException: android.os.BinderProxy.finalize() timed out after 10 seconds  //该方法android.os.BinderProxy.finalize() 10
	<6>[124702.625273]  [0:FinalizerWatchd: 1373] 	at android.os.BinderProxy.destroy(Native Method)
	<6>[124702.625273]  [0:FinalizerWatchd: 1373] 	at android.os.BinderProxy.finalize(Binder.java:690)
	<6>[124702.625273]  [0:FinalizerWatchd: 1373] 	at java.lang.Daemons$FinalizerDaemon.doFinalize(Daemons.java:222)
	<6>[124702.625273]  [0:FinalizerWatchd: 1373] 	at java.lang.Daemons$FinalizerDaemon.run(Daemons.java:209)
	<6>[124702.625273]  [0:FinalizerWatchd: 1373] 	at java.lang.Thread.run(Thread.java:762)


/android/libcore/libart/src/main/java/java/lang/Daemons.java
	
	private static class FinalizerDaemon extends Daemon {
	166        private static final FinalizerDaemon INSTANCE = new FinalizerDaemon();
	167        private final ReferenceQueue<Object> queue = FinalizerReference.queue;
	168        private final AtomicInteger progressCounter = new AtomicInteger(0);
	169        // Object (not reference!) being finalized. Accesses may race!
	170        private Object finalizingObject = null;
	171
	175
	176        @Override public void run() {
	187
	188            // Local copy of progressCounter; saves a fence per increment on ARM and MIPS.
	189            int localProgressCounter = progressCounter.get();
	190
	191            while (isRunning()) {
	192                try {
	193                    // Use non-blocking poll to avoid FinalizerWatchdogDaemon communication
	194                    // when busy.
	195                    FinalizerReference<?> finalizingReference = (FinalizerReference<?>)queue.poll();
	196                    if (finalizingReference != null) {
	197                        finalizingObject = finalizingReference.get();
	198                        progressCounter.lazySet(++localProgressCounter);
	199                    } else {
	200                        finalizingObject = null;
	201                        progressCounter.lazySet(++localProgressCounter);
	202                        // Slow path; block.
	203                        FinalizerWatchdogDaemon.INSTANCE.goToSleep(); //======> 设置watchdogDaemon需要sleep
	204                        finalizingReference = (FinalizerReference<?>)queue.remove();  //====>在这个queue里没有数据时，FinalizerDaemon线程一直在 ReferenceQueue.remove(0)里循环等待；
	205                        finalizingObject = finalizingReference.get();
	206                        progressCounter.set(++localProgressCounter); //========>counter+1,表示FinalizerDaemon运行过一次
	207                        FinalizerWatchdogDaemon.INSTANCE.wakeUp(); //====> 唤醒watchdogDaemon
	208                    }
	209                    doFinalize(finalizingReference);
	210                } catch (InterruptedException ignored) {
	211                } catch (OutOfMemoryError ignored) {
	212                }
	213            }
	214        }
	
	/**
	234     * The watchdog exits the VM if the finalizer ever gets stuck. We consider
	235     * the finalizer to be stuck if it spends more than MAX_FINALIZATION_MILLIS
	236     * on one instance.
	237     */
	238    private static class FinalizerWatchdogDaemon extends Daemon {
	239        private static final FinalizerWatchdogDaemon INSTANCE = new FinalizerWatchdogDaemon();
	240
	241        private boolean needToWork = true;  // Only accessed in synchronized methods.
	242
	243        FinalizerWatchdogDaemon() {
	244            super("FinalizerWatchdogDaemon");
	245        }
	246     
	247        @Override public void run() { //===========核心函数==================
	248            while (isRunning()) {
	249                if (!sleepUntilNeeded()) {
	250                    // We have been interrupted, need to see if this daemon has been stopped.
	251                    continue;
	252                }
	253                final Object finalizing = waitForFinalization(); //=====> 有长时间没有finalize的object
	254                if (finalizing != null && !VMRuntime.getRuntime().isDebuggerActive()) {
	255                    finalizerTimedOut(finalizing); //====> 打印异常后，watchdog退出
	256                    break;
	257                }
	258            }
	259        }
	
	
	261        /**
	262         * Wait until something is ready to be finalized.
	263         * Return false if we have been interrupted
	264         * See also http://code.google.com/p/android/issues/detail?id=22778.
	265         */
	266        private synchronized boolean sleepUntilNeeded() {
	267            while (!needToWork) {
	268                try {
	269                    wait();
	270                } catch (InterruptedException e) {
	271                    // Daemon.stop may have interrupted us.
	272                    return false; 
	273                } catch (OutOfMemoryError e) {
	274                    return false; //oom
	275                }
	276            }
	277            return true; //当needToWork==true 或者被唤醒时(从wait返回), 返回true
	278        }
	
	333        private Object waitForFinalization() {
	334            long startCount = FinalizerDaemon.INSTANCE.progressCounter.get();
	335            // Avoid remembering object being finalized, so as not to keep it alive.
	336            if (!sleepFor(MAX_FINALIZE_NANOS)) { //====> 等待MAX_FINALIZE_NANOS，默认返回true,除非有异常
	337                // Don't report possibly spurious timeout if we are interrupted.
	338                return null;
	339            }
	340            if (getNeedToWork() && FinalizerDaemon.INSTANCE.progressCounter.get() == startCount) { //====>当处于needToWork，且finalizerDaemon的计数器没有变活的情况下

	356                Object finalizing = FinalizerDaemon.INSTANCE.finalizingObject;
	357                sleepFor(NANOS_PER_SECOND / 2);
	358                // Recheck to make it even less likely we report the wrong finalizing object in
	359                // the case which a very slow finalization just finished as we were timing out.
	360                if (getNeedToWork() //====> 再等待
	361                        && FinalizerDaemon.INSTANCE.progressCounter.get() == startCount) { //====>且没有计数器变化
	362                    return finalizing; //======>返回长时间没有finalized 的object
	363                }
	364            }
	365            return null;
	366        }
	
	396    }

      


