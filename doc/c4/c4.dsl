workspace {

    model {
        user = person "Examination Supervisor" "A person of the examination institute, with access to the application."
        
        3ES = softwareSystem "3ES" "Application to scan exam cover pages and aggregate as well as analyze the exam's scores."{
        
            user -> this "Scans exam cover sheets and reviews as well as approves scanned results using"
            
            scanApp = container "Scanning Application" "Frontend application that provides functionality to scan exam cover sheets." "JavaScript / VueJS" {
                user -> this "Scans exam cover sheets using" "HTTPS"
            }
            
            adminApp = container "Admin Application" "Frontend application that provides functionality to review, approve, and export scanned results." "JavaScript / VueJS"  {
                user -> this "Reviews and approves scanned results using" "HTTPS"
            }
            
            apiApp = container "API Application" "Backend application that provides services to save, review and export scanned results." "Python FastAPI" {
            
                scanApp -> this "Makes API calls to" "JSON/HTTPS"
                adminApp -> this "Makes API calls to" "JSON/HTTPS"
                
                apiAppRouter = component "Router" "Provides REST API to the API consumer." "Python FastAPI" {
                    adminApp -> this "Makes API calls to" "JSON/HTTPS"
                    scanApp -> this "Makes API calls to" "JSON/HTTPS"
                }
                
                apiAppAdmin = component "Admin Component" "Provides functionality to review and manipulate scanned results." "Python" {
                    apiAppRouter -> this "Uses"
                }
                
                apiAppScan = component "Scanner Component" "Provides functionality to store the scanned results." "Python" {
                    apiAppRouter -> this "Uses"
                }
                
                apiAppCV = component "Computer Vision Component" "Extracts information from scan." "Python TensorFlow" {
                    apiAppScan -> this "Uses"
                }
                
                apiAppDb = component "Database Handler" "Provides functionality to write and read data records." "Python peewee" {
                    apiAppAdmin -> this "Uses"
                    apiAppScan -> this "Uses"
                }
                
                apiAppFile = component "File Handler" "Provides functionality to store, load, create and export files." "Python os, openpyxl" {
                    apiAppAdmin -> this "Uses"
                    apiAppScan -> this "Uses"
                }
            }
            
            db = container "Database" "Stores student and exam data along with scanned results." "SQLite" {
                tags "Storage"
                apiApp -> this "Reads from and writes to" "Python peewee"
                apiAppDb -> this "Reads from and writes to" "Python peewee"
            }
            
            fd = container "File Storage" "Stores scanned files." "Linux EXT" {
                tags "Storage"
                apiApp -> this "Reads from and writes to" "Python os"
                apiAppFile -> this "Reads from and writes to" "Python os"
            }
        }
    }

    views {

        systemContext 3ES {
            include *
            autolayout tb
        }

        container 3ES {
            include *
            autolayout tb
        }

        component apiApp {
            include *
            autolayout tb
        }

        theme default
        
        styles {
            element "Storage" {
                shape Cylinder
            }
        }
    }

}