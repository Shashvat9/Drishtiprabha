package com.example.drishtiprabha;

import android.os.SystemClock;

import androidx.test.espresso.UiController;
import androidx.test.espresso.ViewAction;
import androidx.test.espresso.action.GeneralClickAction;
import androidx.test.espresso.action.Press;
import androidx.test.espresso.action.Tap;
import androidx.test.espresso.matcher.ViewMatchers;
import androidx.test.rule.ActivityTestRule;

import org.junit.Rule;
import org.junit.Test;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.typeText;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withId;

public class MaximumLoadTest {

    @Rule
    public ActivityTestRule<MainActivity> activityRule = new ActivityTestRule<>(MainActivity.class);

    @Test
    public void simulateMaximumLoad() throws InterruptedException {
        simulateCPULoad();
        simulateMemoryLoad();
        simulateNetworkLoad();
        simulateUIInteraction();
    }

    private void simulateCPULoad() {
        for (int i = 0; i < 100000000; i++) {
            // Perform some CPU-intensive calculations
        }
    }

    private void simulateMemoryLoad() {
        byte[] largeArray = new byte[1024 * 1024 * 100]; // Allocate 100 MB of memory
    }

    private void simulateNetworkLoad() {
        // Simulate a network request
        // You can replace this code with your own network operation
        SystemClock.sleep(3000); // Simulate a 3-second network delay
    }

    private void simulateUIInteraction() throws InterruptedException {
        onView(withId(R.id.otp)).perform(typeText("rajyagurushashvat@gmail.com"), closeSoftKeyboard());
        onView(withId(R.id.password)).perform(typeText("123"), closeSoftKeyboard());
        onView(withId(R.id.bt_sign_in)).perform(click());
        Thread.sleep(5000); // Use Thread.sleep() instead of wait()
        onView(withId(R.id.button)).perform(click());
        onView(withId(R.id.bt_sign_up)).perform(click());
        onView(withId(R.id.name)).perform(typeText("Test"), closeSoftKeyboard());
        onView(withId(R.id.otp)).perform(typeText("test@gmail.com"), closeSoftKeyboard());
        onView(withId(R.id.number)).perform(typeText("1234567890"), closeSoftKeyboard());
        onView(withId(R.id.password)).perform(typeText("test"), closeSoftKeyboard());
        onView(withId(R.id.add)).perform(click());
        Thread.sleep(5000); // Use Thread.sleep() instead of wait()
        onView(withId(R.id.otp)).perform(typeText("test@gmail.com"), closeSoftKeyboard());
        onView(withId(R.id.password)).perform(typeText("test"), closeSoftKeyboard());
        onView(withId(R.id.bt_sign_in)).perform(click());
    }

}
