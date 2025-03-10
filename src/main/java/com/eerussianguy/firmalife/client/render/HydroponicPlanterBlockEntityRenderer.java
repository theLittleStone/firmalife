package com.eerussianguy.firmalife.client.render;

import com.eerussianguy.firmalife.common.blockentities.HydroponicPlanterBlockEntity;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.world.level.material.Fluids;
import net.minecraftforge.fluids.FluidStack;

import net.dries007.tfc.client.RenderHelpers;

public class HydroponicPlanterBlockEntityRenderer extends QuadPlanterBlockEntityRenderer<HydroponicPlanterBlockEntity>
{

    @Override
    public void render(HydroponicPlanterBlockEntity planter, float partialTicks, PoseStack poseStack, MultiBufferSource buffers, int combinedLight, int combinedOverlay)
    {
        RenderHelpers.renderFluidFace(poseStack, new FluidStack(Fluids.WATER, 100), buffers, 1f / 16, 1f / 16, 15f / 16, 15f / 16, 5f / 16, combinedOverlay, combinedLight);

        super.render(planter, partialTicks, poseStack, buffers, combinedLight, combinedOverlay);
    }
}
