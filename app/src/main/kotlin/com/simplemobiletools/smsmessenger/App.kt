package com.simplemobiletools.smsmessenger

import android.app.Application
import com.simplemobiletools.commons.extensions.checkUseEnglish
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform

class App : Application() {
    override fun onCreate() {
        super.onCreate()
        if (! Python.isStarted()) {
            Python.start(AndroidPlatform(applicationContext));
        }
        checkUseEnglish()
    }
}
