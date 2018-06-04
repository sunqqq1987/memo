


IdleHandler接口表示当MessageQueue发现当前没有更多消息可以处理的时候, 则顺便干点别的事情的callback函数(即如果发现idle了, 那就找点别的事干).  callback函数有个boolean的返回值, 表示是否keep. 如果返回false, 则它会在调用完毕之后从mIdleHandlers中移除.

	Looper.myQueue().addIdleHandler(new IdleHandler() {
	
	    @Override
	    public boolean queueIdle() {
	        ...
	        return false;
	    }
	}

# 参考 #

    http://blog.csdn.net/AwayEagle/article/details/50152013
