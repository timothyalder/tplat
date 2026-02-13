import SwiftUI

struct ContentView: View {
    // @State tells SwiftUI to re-render the UI whenever this variable changes
    @State private var count: Int32 = 0

    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "gearshape.fill")
                .imageScale(.large)
                .foregroundColor(.orange)
            
            Text("Rust Counter: \(count)")
                .font(.largeTitle)

            Button(action: {
                print_something_from_rust()
                count = get_and_increment_counter()
            }) {
                Text("Increment via Rust")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
        }
        .frame(width: 300, height: 200)
    }
}

@main
struct FerrisApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}