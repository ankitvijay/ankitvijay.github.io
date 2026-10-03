---
title: "Clean Visual Studio Solution"
date: "2016-10-15T09:39:38+05:30"
lastmod: "2017-09-29T06:13:42+10:00"
url: "/2016/10/15/clean-visual-studio-solution-utility/"
slug: "clean-visual-studio-solution-utility"
wp_id: 1279
category: ["project"]
tag: ["c", "clean-solution", "csproj", "delete-bin", "net", "visual-studio"]
summary: "Today, every project we work on big or small, easy or complex, small team or large team is probably on Source Control. The source control of course can be git, VSTS, SVN etc. Still, there are times where you need to share your code as zip in an email, or shared link. It could be because"
---

Today, every project we work on big or small, easy or complex, small team or large team  is probably on Source Control. The source control of course can be git, VSTS, SVN etc.

Still, there are times where you need to share your code as zip in an email, or shared link. It could be because your customer, colleague or partner do not have access to your source control or simply you have not added your code to Source Control itself.

Now, if you just zip the solution folder and email or share the link then you would include folders like bin, obj, packages or files like *.sou, .*user etc. These files are not required to build the solution. These files increase your zip file size significantly. The solution is simple, delete all the files which are not required. However, what if you have over 50 projects in the solution? And what if you have to this activity multiple times? It is too much of manual effort to do perform this activity.

I had a similar issue in my one of  my engagements recently.  However, instead of spending hours to do this manual work, I decided to automate the process by creating a small console app. The app deletes all the unwanted folders and files recursively from the solution. I have included following folders and files as per my requirements as the part of  deletion list:

```yaml
Folders:  bin, obj, TestResults, packages
Files:  "*.vssscc", "*.ncrunchproject", "*.user", "*.suo"
```

```csharp
namespace SolutionCleaner
{
    using System;
    using System.Collections.Generic;
    using System.IO;

    public class Program
    {
        #region [ Private Fields ]
        private static readonly List<string> FolderList = new List<string> { "bin", "obj", "TestResults", "packages" };
        private static readonly List<string> FileExtensionList = new List<string> { "*.vssscc", "*.ncrunchproject", "*.user", "*.suo" };
        #endregion

        #region [ Private Methods – Main ]
        private static void Main()
        {
            WriteInfo("Enter solution folder. Press enter for current folder.");
            string solutionFolderPath = Console.ReadLine();
            if (string.IsNullOrEmpty(solutionFolderPath?.Trim()))
            {
                solutionFolderPath = Directory.GetCurrentDirectory();
            }

            var solutionFolder = new DirectoryInfo(solutionFolderPath);
            CleanSolution(solutionFolder);
            WriteInfo("Operation completed");
            Console.ReadKey();
        }
        #endregion

        #region [ Private Methods – Clean & Delete ]
        private static void CleanSolution(DirectoryInfo rootFolder)
        {
            foreach (var folder in FolderList)
            {
                DeleteFolder(rootFolder, folder);
            }

            foreach (var file in FileExtensionList)
            {
                DeleteFileByExtention(rootFolder, file);
            }

            WriteInfo("Files/Folders deleted successfully….");
        }

        private static void DeleteFolder(DirectoryInfo rootFolder, string folderName)
        {
            try
            {
                var subfolders = rootFolder.GetDirectories();
                foreach (var subFolder in subfolders)
                {
                    DeleteFolder(subFolder, folderName);
                }

                var isSearchFolder = rootFolder.Name.Equals(folderName, StringComparison.OrdinalIgnoreCase);
                if (!isSearchFolder)
                {
                    return;
                }

                WriteInfo($"Deleting {rootFolder.Name}");
                Directory.Delete(rootFolder.FullName, true);
                WriteSuccess($"Deleted {rootFolder.Name}");
            }
            catch
            {
                WriteError($"Could not delete: {folderName}");
            }
        }

        private static void DeleteFileByExtention(DirectoryInfo rootFolder, string fileExtention)
        {
            try
            {
                var toDelete = rootFolder.GetFiles(fileExtention, SearchOption.AllDirectories);
                foreach (var file in toDelete)
                {
                    WriteInfo($"Deleting {file.FullName}");
                    file.Delete();
                    WriteSuccess($"Deleted {file.FullName}");
                }
            }
            catch (Exception ex)
            {
                WriteError(ex.Message);
            }
        }
        #endregion

        #region [ Private Methods – Write ]
        private static void WriteInfo(string message)
        {
            Write(message);
        }

        private static void WriteSuccess(string message)
        {
            Write(message, ConsoleColor.Green);
        }

        private static void WriteError(string message)
        {
            Write(message, ConsoleColor.Red);
        }

        private static void Write(string message, ConsoleColor consoleColor = ConsoleColor.White)
        {
            Console.ForegroundColor = consoleColor;
            Console.WriteLine(message);
            Console.ResetColor();
        }
        #endregion
    }
}
```

Source code has been shared in GitHub [here](https://github.com/ankitvijay/SolutionCleaner).

Alternatively, You can also download the executable directly from [here](https://1drv.ms/u/s!AuU60N6b3Zh1msN1Qx5tC2VJK-Z4vw).

Hope it helps some you to save your time and be more productive. Please do provide your comments and feedback.
