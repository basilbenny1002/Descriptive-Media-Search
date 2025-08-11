// FileSystemWatcher watcher;

// private void watch()
// {
//   watcher = new FileSystemWatcher();
//   watcher.Path = "C:\Users\basil\Downloads\Programs";
//   watcher.NotifyFilter = NotifyFilters.LastAccess | NotifyFilters.LastWrite
//                          | NotifyFilters.FileName | NotifyFilters.DirectoryName;
//   watcher.Filter = "*.*";
//   watcher.Changed += new FileSystemEventHandler(OnChanged);
//   watcher.EnableRaisingEvents = true;
// }

// private void OnChanged(object source, FileSystemEventArgs e)
// {
//   cout<< "File moved i guess?"
// }

using System;
using System.IO;

class Program
{
    static FileSystemWatcher watcher;

    static void Main()
    {
        watcher = new FileSystemWatcher();
        watcher.Path = @"C:\Users\basil\Downloads\Programs";
        watcher.NotifyFilter = NotifyFilters.FileName | NotifyFilters.DirectoryName;
        watcher.Filter = "*.*";

        watcher.Created += OnCreated;

        watcher.EnableRaisingEvents = true;

        Console.WriteLine("Watching for new files... Press [enter] to exit.");
        Console.ReadLine();
    }

    private static void OnCreated(object sender, FileSystemEventArgs e)
    {
        Console.WriteLine($"New file detected: {e.FullPath}");
    }
}
