#include <stdio.h>
#include "pin.H"

FILE* trace;

// Print a memory read record
VOID RecordMemRead(VOID* ip, UINT32 insSize, UINT32 memOpSize, VOID* addr) {
    fprintf(trace, "%p %u ip\n%p %u addr R\n", ip, insSize, addr, memOpSize);
}

// Print a memory write record
VOID RecordMemWrite(VOID* ip, UINT32 insSize, UINT32 memOpSize, VOID* addr) {
    fprintf(trace, "%p %u ip\n%p %u addr W\n", ip, insSize, addr, memOpSize);
}

// Print a memory read/write record
VOID RecordMemReadWrite(VOID* ip, UINT32 insSize, UINT32 memOpSize, VOID* addr) {
    fprintf(trace, "%p %u ip \n%p %u addr \n", ip, insSize, addr, memOpSize);
}

// Print a record for other instructions
VOID RecordOtherInst(VOID* ip, UINT32 insSize) {
    fprintf(trace, "%p %u ip \n", ip, insSize);
}

// Is called for every instruction and instruments reads and writes
VOID Instruction(INS ins, VOID* v)
{
    // Instruments memory accesses using a predicated call, i.e.
    // the instrumentation is called iff the instruction will actually be executed.
    //
    // On the IA-32 and Intel(R) 64 architectures conditional moves and REP
    // prefixed instructions appear as predicated instructions in Pin.
    UINT32 memOperands = INS_MemoryOperandCount(ins);

    // If the instruction has no memory operands
    if (memOperands == 0) {
        INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)RecordOtherInst, IARG_INST_PTR, IARG_UINT32, INS_Size(ins), IARG_END);
        return;
    }

    // Iterate over each memory operand of the instruction.
    for (UINT32 memOp = 0; memOp < memOperands; memOp++)
    {
        // if (INS_MemoryOperandIsRead(ins, memOp) || INS_MemoryOperandIsWritten(ins, memOp)) {
        //     UINT32 memOpSize = INS_MemoryOperandSize(ins, memOp);
        //     INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)RecordMemReadWrite, IARG_INST_PTR, IARG_UINT32, INS_Size(ins), IARG_UINT32, memOpSize, IARG_MEMORYOP_EA, memOp,
        //                              IARG_END);
        // } else {
        //     INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)RecordOtherInst, IARG_INST_PTR, IARG_UINT32, INS_Size(ins), IARG_END);
        // }
        if (INS_MemoryOperandIsRead(ins, memOp)) {
            UINT32 memOpSize = INS_MemoryOperandSize(ins, memOp);
            INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)RecordMemRead, IARG_INST_PTR, IARG_UINT32, INS_Size(ins), IARG_UINT32, memOpSize, IARG_MEMORYOP_EA, memOp,
                                     IARG_END);
        } else if (INS_MemoryOperandIsWritten(ins, memOp)) {
            UINT32 memOpSize = INS_MemoryOperandSize(ins, memOp);
            INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)RecordMemWrite, IARG_INST_PTR, IARG_UINT32, INS_Size(ins), IARG_UINT32, memOpSize, IARG_MEMORYOP_EA, memOp,
                                     IARG_END);
        } else {
            INS_InsertPredicatedCall(ins, IPOINT_BEFORE, (AFUNPTR)RecordOtherInst, IARG_INST_PTR, IARG_UINT32, INS_Size(ins), IARG_END);
        }
    }
}

VOID Fini(INT32 code, VOID* v)
{
    fprintf(trace, "#eof\n");
    fclose(trace);
}

INT32 Usage()
{
    PIN_ERROR("This Pintool prints a trace of memory addresses\n" + KNOB_BASE::StringKnobSummary() + "\n");
    return -1;
}

int main(int argc, char* argv[])
{
    if (PIN_Init(argc, argv)) return Usage();

    trace = fopen("pinatrace.out", "w");

    INS_AddInstrumentFunction(Instruction, 0);
    PIN_AddFiniFunction(Fini, 0);

    // Never returns
    PIN_StartProgram();

    return 0;
}
