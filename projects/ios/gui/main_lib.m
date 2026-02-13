#import <Cocoa/Cocoa.h>

// Link to your Rust functions
extern int32_t get_and_increment_counter(void);
extern void print_something_from_rust(void);

@interface AppDelegate : NSObject <NSApplicationDelegate>
@property (strong) NSWindow *window;
@property (strong) NSTextField *label;
@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    // 1. Create the Window
    NSRect frame = NSMakeRect(0, 0, 400, 200);
    self.window = [[NSWindow alloc] initWithContentRect:frame
                                              styleMask:(NSWindowStyleMaskTitled | NSWindowStyleMaskClosable | NSWindowStyleMaskResizable)
                                                backing:NSBackingStoreBuffered
                                                  defer:NO];
    [self.window setTitle:@"Rust + AppKit Demo"];
    [self.window center];

    // 2. Create a Label (NSTextField)
    self.label = [[NSTextField alloc] initWithFrame:NSMakeRect(100, 100, 200, 30)];
    [self.label setStringValue:@"Click the button!"];
    [self.label setBezeled:NO];
    [self.label setDrawsBackground:NO];
    [self.label setEditable:NO];
    [self.label setAlignment:NSTextAlignmentCenter];
    [[self.window contentView] addSubview:self.label];

    // 3. Create a Button
    NSButton *button = [[NSButton alloc] initWithFrame:NSMakeRect(125, 50, 150, 30)];
    [button setTitle:@"Increment Rust"];
    [button setButtonType:NSButtonTypeMomentaryPushIn];
    [button setBezelStyle:NSBezelStyleRounded];
    [button setTarget:self];
    [button setAction:@selector(buttonClicked:)];
    [[self.window contentView] addSubview:button];

    [self.window makeKeyAndOrderFront:nil];
    [NSApp activateIgnoringOtherApps:YES];
}

- (void)buttonClicked:(id)sender {
    print_something_from_rust(); // Call Rust
    int32_t count = get_and_increment_counter(); // Call Rust
    [self.label setStringValue:[NSString stringWithFormat:@"Rust Counter: %d", count]];
}

@end

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSApplication *app = [NSApplication sharedApplication];
        AppDelegate *delegate = [[AppDelegate alloc] init];
        [app setDelegate:delegate];
        [app run];
    }
    return 0;
}