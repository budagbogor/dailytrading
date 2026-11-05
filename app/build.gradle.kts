plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android { namespace = "id.quantsyariah"; compileSdk = 35
    defaultConfig { applicationId = "id.quantsyariah"; minSdk = 26; targetSdk = 35; versionCode = 19; versionName = "1.9.0" }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_17; targetCompatibility = JavaVersion.VERSION_17 }
    kotlinOptions { jvmTarget = "17" }
}
