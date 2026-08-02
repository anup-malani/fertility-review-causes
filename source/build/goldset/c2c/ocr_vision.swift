// ocr_vision.swift — OCR image files using the macOS Vision framework.
//
// Used for the C.2.c Korean public-rental-housing paper, which is a 21-page image-only scan with no
// text layer. Vision is built into macOS and supports Korean, so this needs no third-party install
// (no tesseract, no brew) — it uses a capability the machine already has.
//
//   swiftc -O ocr_vision.swift -o ocr_vision
//   ./ocr_vision --languages                 # list supported recognition languages
//   ./ocr_vision page-01.png page-02.png ... # OCR each, print text with page separators

import Foundation
import Vision
import AppKit

let args = Array(CommandLine.arguments.dropFirst())

if args.first == "--languages" {
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    if let langs = try? req.supportedRecognitionLanguages() {
        print(langs.joined(separator: " "))
    }
    exit(0)
}

// Prefer Korean, fall back to English for the abstract/references which are often bilingual.
let preferred = ["ko-KR", "en-US"]

for path in args {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        FileHandle.standardError.write("SKIP (unreadable): \(path)\n".data(using: .utf8)!)
        continue
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    let supported = (try? request.supportedRecognitionLanguages()) ?? []
    request.recognitionLanguages = preferred.filter { supported.contains($0) }

    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do {
        try handler.perform([request])
        let obs = request.results ?? []
        let text = obs.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
        print("=== \(URL(fileURLWithPath: path).lastPathComponent) ===")
        print(text)
    } catch {
        FileHandle.standardError.write("FAIL \(path): \(error)\n".data(using: .utf8)!)
    }
}
