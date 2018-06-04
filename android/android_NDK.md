# Android NDK #

	参考：https://developer.android.com/ndk/guides/concepts.html
		 https://developer.android.com/ndk/guides/ndk-build.html

	调试您的应用： https://developer.android.com/studio/debug/index.html

	Android NDK 是一组允许您将 C 或 C++（“原生代码”）嵌入到 Android 应用中的工具。 
	能够在 Android 应用中使用原生代码对于想执行以下一项或多项操作的开发者特别有用：
	    在平台之间移植其应用。
	    重复使用现有库，或者提供其自己的库供重复使用。
	    在某些情况下提高性能，特别是像游戏这种计算密集型应用。
	
- linux下的NDK环境搭建

		https://www.cnblogs.com/fengfeng/p/3299062.html

- **windows下Android Studio+NDK环境搭建**
	
	- 参考
			
			https://blog.csdn.net/yehui928186846/article/details/52787773
			添加 C 和 C++ 代码： https://developer.android.com/studio/projects/add-native-code.html
	
	- NDK工具链路径

			\Sdk\ndk-bundle\toolchains\aarch64-linux-android-4.9\prebuilt\windows-x86_64\bin\
			aarch64-linux-android-gcc.exe

	- 查看NDK的安装路径
	
			file->project structure中看到NDK location,如：
			C:\Users\Administrator\AppData\Local\Android\Sdk\ndk-bundle

			同时项目的local.properties配置文件中也有一样的路径：
			ndk.dir=C\:\\Users\\Administrator\\AppData\\Local\\Android\\Sdk\\ndk-bundle
			
	- NDK开发环境搭建
	
			参考：https://www.jianshu.com/p/a37782b56770

			1）在AS中用SDK manager安装NDK

			2）AS3.0需要在gradle.properties文件中加上一行:
				android.useDeprecatedNdk=true

			3）在包下，添加对应jni接口的java封装类，并自动加载jni lib:
				static {
			        System.loadLibrary("jnitest_Lib"); //to be loaded lib: lib.so
			    }

			4）使用ExternalTools添加"javah -jni"编译快捷方式
			它会根据java文件名与方法名, 生成包含对应的C/C++里面的方法名的.h文件
			注意：java文件中不能有中文字符,否则报错
			其中：
				Program: $JDKPath$\bin\javah.exe 这里配置的是JDK目录下的javah.exe的路径
				Parametes: -classpath . -jni -d $ModuleFileDir$/src/main/jni $FileClass$
					$FileClass$指的是要执行操作的类名（即我们操作的文件），
					$ModuleFileDir$/src/main/jni表示生成的文件保存在这个module目录的src/main/jni目录下
				Working: $ModuleFileDir$\src\main\java 表示module目录下的src\main\java目录
			
			使用方式：
				选中java文件—>右键—>External Tools—>javah-jni，将生成jni文件夹以及文件夹下的包名.类名的.h头文件

			5）jni目录下添加jni的c/c++实现,已经为编译规则文件：Android.mk，Application.mk

			6）编译出so库

			方法有：

			（1) 在app/build.gradle中使用ndkBuild配置编译方法后,build project
				先注释掉cmake相关的项，再添加如下：
				defaultConfig {
					externalNativeBuild {
			            ndk {
			                //cFlags=
			                moduleName"jnitest_Lib" //生成 libjnitest_Lib.so
			                //ldLibs "log", "z", "m"
			                abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64"  //对应APP_ABI
			            }
					}
				}
			
				externalNativeBuild {
			        ndkBuild{
			            path "src/main/jni/Android.mk"
			
			        }
			    }

			（2）也可以使用ExternalTools添加ndk-build快捷方式生成so库
				其中:
				Program: F:\apk\sdk\ndk-bundle\ndk-build.cmd 这里配置的是ndk下的ndk-build.cmd的路径
				Working: $ModuleFileDir$\src\main\

				使用方式：
				选中C/C++文件—>右键—>ExternalTools—>ndk-build，将在main文件夹下生成libs文件夹以及多个so文件
	
- issue

	- 警告"Android NDK: WARNING: APP_PLATFORM android-14 is larger than android:minSdkVersion 8"
	
			https://blog.csdn.net/asmcvc/article/details/33722115