//
//  Item.swift
//  LiveScan-App
//
//  Created by slk on 09/12/2024.
//

import Foundation
import SwiftData

@Model
final class Item {
    var timestamp: Date
    
    init(timestamp: Date) {
        self.timestamp = timestamp
    }
}
