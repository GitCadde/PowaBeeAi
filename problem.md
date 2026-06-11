Feedback Type:
Frown (Error)

Timestamp:
2026-06-11T12:54:08.5079421Z

Local Time:
2026-06-11T14:54:08.5079421+02:00

Session ID:
95248a79-4b00-403c-822d-140bb18e07cf

Release:
May 2026

Product Version:
2.154.1260.0 (26.05)+f6b01d4ee0491b332167366c6bb36121ee062561 (x64)

Error Message:
Fehler beim Rendern des Berichts.

Stack Trace:
JavaScript:TypeError
at https://ms-pbi.pbi.microsoft.com/minerva/scripts/desktop.PivotTableVisuals.min.js:1:535662
    at baseFindIndex (https://ms-pbi.pbi.microsoft.com/minerva/scripts/powerbi.common.externals.js:25215:11)
    at findIndex (https://ms-pbi.pbi.microsoft.com/minerva/scripts/powerbi.common.externals.js:31751:14)
    at lodash.find (https://ms-pbi.pbi.microsoft.com/minerva/scripts/powerbi.common.externals.js:29550:21)
    at TableExColumnHierarchyNavigator.getColumnIndexFromQueryName (https://ms-pbi.pbi.microsoft.com/minerva/scripts/desktop.PivotTableVisuals.min.js:1:535630)
    at TablixRendererMid.getPrefixCellBinding (https://ms-pbi.pbi.microsoft.com/minerva/scripts/desktop.PivotTableVisuals.min.js:1:201555)
    at TablixRendererMid.getPrefixBindings (https://ms-pbi.pbi.microsoft.com/minerva/scripts/desktop.PivotTableVisuals.min.js:1:191785)
    at TablixRendererMid.getRowGroupBindings (https://ms-pbi.pbi.microsoft.com/minerva/scripts/desktop.PivotTableVisuals.min.js:1:190912)
    at TablixRendererMid.insertRowGroup (https://ms-pbi.pbi.microsoft.com/minerva/scripts/desktop.PivotTableVisuals.min.js:1:189172)
    at https://ms-pbi.pbi.microsoft.com/minerva/scripts/desktop.PivotTableVisuals.min.js:1:187455

Stack Trace Message:
Fehler beim Rendern des Berichts.

Invocation Stack Trace:
   bei Microsoft.Mashup.Host.Document.ExceptionExtensions.GetCurrentInvocationStackTrace()
   bei Microsoft.Mashup.Client.UI.Shared.StackTraceInfo..ctor(String exceptionStackTrace, String invocationStackTrace, String exceptionMessage)
   bei Microsoft.PowerBI.Client.Windows.Telemetry.PowerBIUserFeedbackServices.GetStackTraceInfo(Exception e)
   bei Microsoft.PowerBI.Client.Windows.Telemetry.PowerBIUserFeedbackServices.ReportException(IWindowHandle activeWindow, IUIHost uiHost, FeedbackPackageInfo feedbackPackageInfo, Exception e, Boolean useGDICapture)
   bei Microsoft.Mashup.Client.UI.Shared.UnexpectedExceptionHandler.<>c__DisplayClass14_0.<HandleException>b__0()
   bei Microsoft.Mashup.Client.UI.Shared.UnexpectedExceptionHandler.HandleException(Exception e)
   bei Microsoft.PowerBI.Client.PowerBIUnexpectedExceptionHandler.HandleException(Exception e)
   bei System.RuntimeMethodHandle.InvokeMethod(Object target, Object[] arguments, Signature sig, Boolean constructor)
   bei System.Reflection.RuntimeMethodInfo.UnsafeInvokeInternal(Object obj, Object[] parameters, Object[] arguments)
   bei System.Reflection.RuntimeMethodInfo.Invoke(Object obj, BindingFlags invokeAttr, Binder binder, Object[] parameters, CultureInfo culture)
   bei Microsoft.PowerBI.Client.Windows.WebView2.WebView2Interop.<>c__DisplayClass36_0.<InvokeCsMethod>b__0()
   bei Microsoft.PowerBI.Client.Windows.WebView2.WebView2Interop.<>c__DisplayClass39_0`1.<RunAsync>b__0(Object s)
   bei System.RuntimeMethodHandle.InvokeMethod(Object target, Object[] arguments, Signature sig, Boolean constructor)
   bei System.Reflection.RuntimeMethodInfo.UnsafeInvokeInternal(Object obj, Object[] parameters, Object[] arguments)
   bei System.Delegate.DynamicInvokeImpl(Object[] args)
   bei System.Windows.Forms.Control.InvokeMarshaledCallbackDo(ThreadMethodEntry tme)
   bei System.Windows.Forms.Control.InvokeMarshaledCallbackHelper(Object obj)
   bei System.Threading.ExecutionContext.RunInternal(ExecutionContext executionContext, ContextCallback callback, Object state, Boolean preserveSyncCtx)
   bei System.Threading.ExecutionContext.Run(ExecutionContext executionContext, ContextCallback callback, Object state, Boolean preserveSyncCtx)
   bei System.Threading.ExecutionContext.Run(ExecutionContext executionContext, ContextCallback callback, Object state)
   bei System.Windows.Forms.Control.InvokeMarshaledCallback(ThreadMethodEntry tme)
   bei System.Windows.Forms.Control.InvokeMarshaledCallbacks()
   bei System.Windows.Forms.Control.WndProc(Message& m)
   bei System.Windows.Forms.NativeWindow.Callback(IntPtr hWnd, Int32 msg, IntPtr wparam, IntPtr lparam)
   bei System.Windows.Forms.UnsafeNativeMethods.DispatchMessageW(MSG& msg)
   bei System.Windows.Forms.UnsafeNativeMethods.DispatchMessageW(MSG& msg)
   bei System.Windows.Forms.Application.ComponentManager.System.Windows.Forms.UnsafeNativeMethods.IMsoComponentManager.FPushMessageLoop(IntPtr dwComponentID, Int32 reason, Int32 pvLoopData)
   bei System.Windows.Forms.Application.ThreadContext.RunMessageLoopInner(Int32 reason, ApplicationContext context)
   bei System.Windows.Forms.Application.ThreadContext.RunMessageLoop(Int32 reason, ApplicationContext context)
   bei System.Windows.Forms.Form.ShowDialog(IWin32Window owner)
   bei Microsoft.Mashup.Client.UI.Shared.WindowManager.ShowModal[T](T dialog, Func`1 showModalFunction)
   bei Microsoft.PowerBI.Client.AppModule.<>c__DisplayClass4_0.<Run>b__0()
   bei Microsoft.PowerBI.Client.Windows.IExceptionHandlerExtensions.<>c__DisplayClass3_0.<HandleExceptionsWithNestedTasks>b__0()
   bei Microsoft.Mashup.Host.Document.ExceptionHandlerExtensions.HandleExceptions(IExceptionHandler exceptionHandler, Action action)
   bei Microsoft.PowerBI.Client.AppModule.Run()
   bei Microsoft.PowerBI.Client.Program.RunApplicationFlow(String[] args, IPowerBIRootTrace trace)
   bei Microsoft.PowerBI.Client.Program.Main(String[] args)


JS Error Message:
Cannot read properties of undefined (reading 'queryName')

PowerBINonFatalError:
{"AppName":"PBIDesktop","AppVersion":"2.154.1260.0","ModuleName":"https://ms-pbi.pbi.microsoft.com/minerva/scripts/desktop.PivotTableVisuals.min.js","Component":"","Error":"TypeError","MethodDef":"","ErrorOffset":"1:535662","ErrorCode":""}

OS Version:
Microsoft Windows NT 10.0.26200.0 (x64 de-DE)

CLR Version:
4.8 or later [Release Number = 533509]

Peak Virtual Memory:
86.6 GB

Private Memory:
640 MB

Peak Working Set:
846 MB

IE Version:
11.1882.26100.0

User ID:
7d41ee3c-43f6-4ce2-84a4-4bf4976a0b5a

Workbook Package Info:
1* - de-DE, Query Groups: 0, fastCombine: Disabled, runBackgroundAnalysis: False.

Telemetry Enabled:
True

Snapshot Trace Logs:
C:\Users\vw7sysb\Microsoft\Power BI Desktop Store App\FrownSnapShotb55c9166-5849-4c9d-bd01-6a3e68138013.zip

Model Default Mode:
Import

Model Version:
PowerBI_V3

Performance Trace Logs:
C:\Users\vw7sysb\Microsoft\Power BI Desktop Store App\PerformanceTraces.zip

Enabled Preview Features:
PBI_DatabricksAdbcVersionEnabled
PBI_googleBigQueryAdbcVersionEnabled
PBI_scorecardVisual
PBI_setLabelOnExportPdf
PBI_oneDriveSave
PBI_oneDriveShare
PBI_useModernPublishDialogs
PBI_gitIntegration
PBI_tmdlInDataset
PBI_enhancedReportFormat
PBI_enhancedReportFormatPBIX
PBI_advancedSlicerTypeList
PBI_useModernMashupEditor
PBI_aiNarrativesVisual
PBI_copilotUnifiedTooling
MashupFlight_EnableOracleBundledOdacProviderV2
PBI_sqlDbNativeArtifactsOnDesktop
PBI_enableExportQueries

Disabled Preview Features:
PBI_UseRedshiftODBCV2
PQ_UseBaseViewXmlForSharePoint
PBI_snowflakeLegacyOdbcVersionEnabled
PBI_shapeMapVisualEnabled
PBI_SpanishLinguisticsEnabled
PBI_qnaLiveConnect
PBI_b2bExternalDatasetSharing
PBI_onObject
PBI_publishDialogsSupportSubfolders
PBI_qnaImproveLsdlCopilot
PBI_customCalendars
PBI_enableOracleBundledOdacProviderForDQ
PBI_supportUDFs
PBI_dynamicCalcColumn
PBI_newVisualDefaults2026

Disabled DirectQuery Options:
TreatHanaAsRelationalSource

Cloud:
GlobalCloud

PowerBIUserFeedbackServices_IsReported:
True

DPI Scale:
100%

Supported Services:
Power BI

Formulas:


section Section1;

shared fakt_chpu = let
  Quelle = PowerPlatform.Dataflows([]),
  #"Navigation 1" = Quelle{[Id = "Workspaces"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[workspaceId = "c5f886de-fae0-47a0-a39c-88802ced5740"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[dataflowId = "f86c3ce9-edc9-4f19-a809-f03028f2103b"]}[Data],
  #"Navigation 4" = #"Navigation 3"{[entity = "fakt_chpu", version = ""]}[Data],

  // ─────────────────────────────────────────────────────────────────────
  // Simulation der künftigen Dataflow-Spalten (YTD/VSI je Werk × KW).
  // Sobald der Dataflow diese Spalten selbst liefert, entfallen alle
  // Schritte ab hier ersatzlos (gleiche Spaltennamen).
  // ─────────────────────────────────────────────────────────────────────
  MitJahr = Table.AddColumn(#"Navigation 4", "_jahr", each Number.IntegerDivide([jahr_kw], 100), Int64.Type),

  Gruppiert = Table.Group(
    MitJahr,
    {"source_plant_id", "_jahr"},
    {{"_grp", (t) =>
      let
        Sortiert = Table.Sort(t, {{"jahr_kw", Order.Ascending}}),
        MitYtd = Table.AddColumn(
          Sortiert,
          "_ytd",
          (zeile) =>
            let
              Bis = Table.SelectRows(Sortiert, each [jahr_kw] <= zeile[jahr_kw])
            in
              [
                ze_ist_ytd = List.Sum(Bis[ze_ist]),
                ze_soll_ytd = List.Sum(Bis[ze_soll]),
                anmin_ist_ytd = List.Sum(Bis[anmin_ist]),
                anmin_soll_ytd = List.Sum(Bis[anmin_soll]),
                anmin_soll_ohne_ratio_ytd = List.Sum(Bis[anmin_soll_ohne_ratio]),
                anmin_ist_d_ytd = List.Sum(Bis[anmin_ist_d]),
                anmin_ist_di_ytd = List.Sum(Bis[anmin_ist_di]),
                anmin_ist_i_ytd = List.Sum(Bis[anmin_ist_i]),
                anmin_soll_d_ytd = List.Sum(Bis[anmin_soll_d]),
                anmin_soll_di_ytd = List.Sum(Bis[anmin_soll_di]),
                anmin_soll_i_ytd = List.Sum(Bis[anmin_soll_i]),
                anmin_soll_ohne_ratio_d_ytd = List.Sum(Bis[anmin_soll_ohne_ratio_d]),
                anmin_soll_ohne_ratio_di_ytd = List.Sum(Bis[anmin_soll_ohne_ratio_di]),
                anmin_soll_ohne_ratio_i_ytd = List.Sum(Bis[anmin_soll_ohne_ratio_i])
              ]
        ),
        Expandiert = Table.ExpandRecordColumn(
          MitYtd,
          "_ytd",
          {"ze_ist_ytd", "ze_soll_ytd", "anmin_ist_ytd", "anmin_soll_ytd", "anmin_soll_ohne_ratio_ytd", "anmin_ist_d_ytd", "anmin_ist_di_ytd", "anmin_ist_i_ytd", "anmin_soll_d_ytd", "anmin_soll_di_ytd", "anmin_soll_i_ytd", "anmin_soll_ohne_ratio_d_ytd", "anmin_soll_ohne_ratio_di_ytd", "anmin_soll_ohne_ratio_i_ytd"}
        )
      in
        Expandiert,
      type table}}
  ),

  Kombiniert = Table.Combine(Gruppiert[_grp]),

  // Abgeleitete YTD-Kennzahlen (CHPU/Ratio) auf Zeilenebene
  ChpuIstYtd = Table.AddColumn(Kombiniert, "chpu_ist_ytd", each if [ze_ist_ytd] = null or [ze_ist_ytd] = 0 then null else [anmin_ist_ytd] / [ze_ist_ytd], type nullable number),
  ChpuSollYtd = Table.AddColumn(ChpuIstYtd, "chpu_soll_ytd", each if [ze_ist_ytd] = null or [ze_ist_ytd] = 0 then null else [anmin_soll_ytd] / [ze_ist_ytd], type nullable number),
  Chpu0Ytd = Table.AddColumn(ChpuSollYtd, "chpu_soll_ohne_ratio_ytd", each if [ze_ist_ytd] = null or [ze_ist_ytd] = 0 then null else [anmin_soll_ohne_ratio_ytd] / [ze_ist_ytd], type nullable number),
  RatioIstYtd = Table.AddColumn(Chpu0Ytd, "ratio_ist_ytd", each if [anmin_soll_ohne_ratio_ytd] = null or [anmin_soll_ohne_ratio_ytd] = 0 then null else ([anmin_soll_ohne_ratio_ytd] - [anmin_ist_ytd]) / [anmin_soll_ohne_ratio_ytd] * 100, type nullable number),
  RatioSollYtd = Table.AddColumn(RatioIstYtd, "ratio_soll_ytd", each if [anmin_soll_ohne_ratio_ytd] = null or [anmin_soll_ohne_ratio_ytd] = 0 then null else ([anmin_soll_ohne_ratio_ytd] - [anmin_soll_ytd]) / [anmin_soll_ohne_ratio_ytd] * 100, type nullable number),

  // VSI = YTD (temporäre Logik, bis finale VSI-Definition abgestimmt ist)
  ZeIstVsi = Table.AddColumn(RatioSollYtd, "ze_ist_vsi", each [ze_ist_ytd], type nullable number),
  ZeSollVsi = Table.AddColumn(ZeIstVsi, "ze_soll_vsi", each [ze_soll_ytd], type nullable number),
  AnminIstVsi = Table.AddColumn(ZeSollVsi, "anmin_ist_vsi", each [anmin_ist_ytd], type nullable number),
  AnminSollVsi = Table.AddColumn(AnminIstVsi, "anmin_soll_vsi", each [anmin_soll_ytd], type nullable number),
  AnminSoll0Vsi = Table.AddColumn(AnminSollVsi, "anmin_soll_ohne_ratio_vsi", each [anmin_soll_ohne_ratio_ytd], type nullable number),
  ChpuIstVsi = Table.AddColumn(AnminSoll0Vsi, "chpu_ist_vsi", each [chpu_ist_ytd], type nullable number),
  ChpuSollVsi = Table.AddColumn(ChpuIstVsi, "chpu_soll_vsi", each [chpu_soll_ytd], type nullable number),
  RatioIstVsi = Table.AddColumn(ChpuSollVsi, "ratio_ist_vsi", each [ratio_ist_ytd], type nullable number),
  RatioSollVsi = Table.AddColumn(RatioIstVsi, "ratio_soll_vsi", each [ratio_soll_ytd], type nullable number),

  OhneJahr = Table.RemoveColumns(RatioSollVsi, {"_jahr"}),

  Typisiert = Table.TransformColumnTypes(
    OhneJahr,
    {
      {"ze_ist_ytd", type nullable number}, {"ze_soll_ytd", type nullable number},
      {"anmin_ist_ytd", type nullable number}, {"anmin_soll_ytd", type nullable number},
      {"anmin_soll_ohne_ratio_ytd", type nullable number},
      {"anmin_ist_d_ytd", type nullable number}, {"anmin_ist_di_ytd", type nullable number}, {"anmin_ist_i_ytd", type nullable number},
      {"anmin_soll_d_ytd", type nullable number}, {"anmin_soll_di_ytd", type nullable number}, {"anmin_soll_i_ytd", type nullable number},
      {"anmin_soll_ohne_ratio_d_ytd", type nullable number}, {"anmin_soll_ohne_ratio_di_ytd", type nullable number}, {"anmin_soll_ohne_ratio_i_ytd", type nullable number}
    }
  )
in
  Typisiert;

shared fakt_chpu_kst = let
  Quelle = PowerPlatform.Dataflows([]),
  #"Navigation 1" = Quelle{[Id = "Workspaces"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[workspaceId = "c5f886de-fae0-47a0-a39c-88802ced5740"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[dataflowId = "f86c3ce9-edc9-4f19-a809-f03028f2103b"]}[Data],
  #"Navigation 4" = #"Navigation 3"{[entity = "fakt_chpu_kst", version = ""]}[Data],

  // ─────────────────────────────────────────────────────────────────────
  // Simulation der künftigen Dataflow-Spalten (YTD je Werk × KST × KW).
  // Sobald der Dataflow diese Spalten selbst liefert, entfallen alle
  // Schritte ab hier ersatzlos (gleiche Spaltennamen).
  // ─────────────────────────────────────────────────────────────────────
  MitJahr = Table.AddColumn(#"Navigation 4", "_jahr", each Number.IntegerDivide([jahr_kw], 100), Int64.Type),

  Gruppiert = Table.Group(
    MitJahr,
    {"source_plant_id", "kst_bezeichnung_kurz", "_jahr"},
    {{"_grp", (t) =>
      let
        Sortiert = Table.Sort(t, {{"jahr_kw", Order.Ascending}}),
        MitYtd = Table.AddColumn(
          Sortiert,
          "_ytd",
          (zeile) =>
            let
              Bis = Table.SelectRows(Sortiert, each [jahr_kw] <= zeile[jahr_kw])
            in
              [
                ze_ist_ytd = List.Sum(Bis[ze_ist]),
                ze_soll_ytd = List.Sum(Bis[ze_soll]),
                anmin_ist_ytd = List.Sum(Bis[anmin_ist]),
                anmin_soll_ytd = List.Sum(Bis[anmin_soll]),
                anmin_soll_ohne_ratio_ytd = List.Sum(Bis[anmin_soll_ohne_ratio])
              ]
        ),
        Expandiert = Table.ExpandRecordColumn(
          MitYtd,
          "_ytd",
          {"ze_ist_ytd", "ze_soll_ytd", "anmin_ist_ytd", "anmin_soll_ytd", "anmin_soll_ohne_ratio_ytd"}
        )
      in
        Expandiert,
      type table}}
  ),

  Kombiniert = Table.Combine(Gruppiert[_grp]),

  // Abgeleitete YTD-Kennzahlen (CHPU/Ratio) auf Zeilenebene
  ChpuIstYtd = Table.AddColumn(Kombiniert, "chpu_ist_ytd", each if [ze_ist_ytd] = null or [ze_ist_ytd] = 0 then null else [anmin_ist_ytd] / [ze_ist_ytd], type nullable number),
  ChpuSollYtd = Table.AddColumn(ChpuIstYtd, "chpu_soll_ytd", each if [ze_ist_ytd] = null or [ze_ist_ytd] = 0 then null else [anmin_soll_ytd] / [ze_ist_ytd], type nullable number),
  RatioIstYtd = Table.AddColumn(ChpuSollYtd, "ratio_ist_ytd", each if [anmin_soll_ohne_ratio_ytd] = null or [anmin_soll_ohne_ratio_ytd] = 0 then null else ([anmin_soll_ohne_ratio_ytd] - [anmin_ist_ytd]) / [anmin_soll_ohne_ratio_ytd] * 100, type nullable number),
  RatioSollYtd = Table.AddColumn(RatioIstYtd, "ratio_soll_ytd", each if [anmin_soll_ohne_ratio_ytd] = null or [anmin_soll_ohne_ratio_ytd] = 0 then null else ([anmin_soll_ohne_ratio_ytd] - [anmin_soll_ytd]) / [anmin_soll_ohne_ratio_ytd] * 100, type nullable number),

  OhneJahr = Table.RemoveColumns(RatioSollYtd, {"_jahr"}),

  Typisiert = Table.TransformColumnTypes(
    OhneJahr,
    {
      {"ze_ist_ytd", type nullable number}, {"ze_soll_ytd", type nullable number},
      {"anmin_ist_ytd", type nullable number}, {"anmin_soll_ytd", type nullable number},
      {"anmin_soll_ohne_ratio_ytd", type nullable number}
    }
  )
in
  Typisiert;

WebView2 Runtime Version:
149.0.4022.62

WebView2 SDK Version:
1.0.2365.46